#!/usr/bin/env python3
"""Rapproche un fichier d'établissements d'un export CRM.

Python standard uniquement, aucune installation.

    python3 dedup.py --fichier etablissements.csv --crm export-crm.csv

Sorties, dans le dossier courant (ou --sortie) :
    rapprochement.csv   une ligne par établissement du fichier, avec le verdict
    rapport.txt         le compte, clé par clé

Quatre clés, essayées dans cet ordre. La première qui répond gagne.
    1. SIRET             exact, 14 chiffres                       -> oui
    2. Téléphone         normalisé au format international        -> oui
    3. Domaine du site   seulement s'il est propre à l'établissement -> oui
    4. Nom + code postal nom nettoyé, même code postal            -> à vérifier

Le script ne modifie aucun des deux fichiers d'entrée.
"""

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

# En-têtes reconnus dans un export CRM, en minuscules et sans accents.
# L'ordre compte : le premier en-tête trouvé est retenu.
ALIAS = {
    "siret": ["siret", "numero siret", "n siret", "siret number"],
    "telephone": [
        "telephone", "tel", "phone", "phone number", "numero de telephone",
        "telephone principal", "company phone", "standard", "mobile",
        "mobile phone number", "telephone fixe",
    ],
    "site": [
        "site web", "site", "website", "website url", "url du site web",
        "company domain name", "nom de domaine de l'entreprise", "domaine", "domain",
    ],
    "nom": [
        "nom", "name", "company name", "nom de l'entreprise", "nom de l'entreprise",
        "entreprise", "societe", "raison sociale", "account name", "organisation",
    ],
    "code_postal": ["code postal", "cp", "postal code", "zip", "zip code", "code postal de l'entreprise"],
    "id": ["record id", "id", "id fiche", "id de fiche", "company id", "account id", "hs_object_id"],
    "proprietaire": [
        "proprietaire", "owner", "company owner", "proprietaire de l'entreprise",
        "proprietaire du contact", "contact owner", "account owner",
    ],
}

# Mots retirés d'un nom avant comparaison : formes juridiques et mots vides.
MOTS_VIDES = {
    "sarl", "sas", "sasu", "eurl", "sa", "ei", "eirl", "sci", "snc", "ets",
    "etablissements", "etablissement", "societe", "ste", "le", "la", "les",
    "de", "du", "des", "d", "l", "et", "and", "the",
}


def sans_accents(texte):
    return "".join(
        c for c in unicodedata.normalize("NFKD", texte or "") if not unicodedata.combining(c)
    )


def cle_entete(texte):
    t = sans_accents(texte).lower().replace("’", "'")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9' ]", " ", t)).strip()


def norm_siret(valeur):
    chiffres = re.sub(r"\D", "", valeur or "")
    return chiffres if len(chiffres) == 14 else ""


def norm_telephone(valeur, indicatif="33"):
    """Ramène un numéro au format international sans le +, ou '' s'il est inexploitable.

    02 54 55 22 22, +33 2 54 55 22 22, 0033254552222 et 33254552222 donnent tous
    33254552222. Une cellule qui contient plusieurs numéros ne garde que le premier.
    """
    brut = (valeur or "").strip()
    if not brut:
        return ""
    brut = re.split(r"[;/|,]| ou ", brut)[0]
    plus = brut.lstrip().startswith("+")
    chiffres = re.sub(r"\D", "", brut)
    if not chiffres:
        return ""
    if chiffres.startswith("00"):
        chiffres = chiffres[2:]
    elif plus:
        pass
    elif chiffres.startswith("0") and len(chiffres) == 10:
        chiffres = indicatif + chiffres[1:]
    elif len(chiffres) == 9 and not chiffres.startswith("0"):
        chiffres = indicatif + chiffres
    # +33 (0)2 54 ... : un zéro parasite après l'indicatif
    if chiffres.startswith(indicatif + "0") and len(chiffres) == len(indicatif) + 10:
        chiffres = indicatif + chiffres[len(indicatif) + 1:]
    return chiffres if 8 <= len(chiffres) <= 15 else ""


def norm_domaine(valeur):
    v = (valeur or "").strip().lower()
    if not v:
        return ""
    v = re.sub(r"^[a-z]+://", "", v)
    v = v.split("/")[0].split("?")[0].split(":")[0]
    v = re.sub(r"^www\.", "", v)
    return v if "." in v else ""


def norm_nom(valeur):
    t = sans_accents(valeur).lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    mots = [m for m in t.split() if m not in MOTS_VIDES]
    return " ".join(mots)


def norm_cp(valeur):
    chiffres = re.sub(r"\D", "", valeur or "")
    if len(chiffres) == 4:  # le zéro initial mangé par un tableur
        chiffres = "0" + chiffres
    return chiffres if len(chiffres) == 5 else ""


def lire_csv(chemin):
    brut = Path(chemin).read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            texte = brut.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    premiere = texte.split("\n", 1)[0]
    sep = max([",", ";", "\t"], key=premiere.count)
    lignes = list(csv.reader(texte.splitlines(), delimiter=sep))
    if not lignes:
        sys.exit(f"{chemin} est vide.")
    entetes = [e.strip() for e in lignes[0]]
    donnees = [dict(zip(entetes, l + [""] * (len(entetes) - len(l)))) for l in lignes[1:] if any(c.strip() for c in l)]
    return entetes, donnees


def trouver_colonne(entetes, champ, force=None):
    if force:
        if force not in entetes:
            sys.exit(f"Colonne « {force} » introuvable. En-têtes disponibles : {', '.join(entetes)}")
        return force
    index = {cle_entete(e): e for e in entetes}
    for alias in ALIAS[champ]:
        if alias in index:
            return index[alias]
    return None


def main():
    p = argparse.ArgumentParser(description="Rapproche un fichier d'établissements d'un export CRM.")
    p.add_argument("--fichier", required=True, help="CSV des établissements (l'onglet Établissements exporté)")
    p.add_argument("--crm", required=True, help="CSV exporté du CRM (entreprises ou contacts)")
    p.add_argument("--sortie", default=".", help="dossier de sortie (défaut : dossier courant)")
    p.add_argument("--indicatif", default="33", help="indicatif pays par défaut, sans le + (défaut : 33)")
    p.add_argument("--id-fichier", default="ID Scalon", help="colonne identifiant du fichier (défaut : ID Scalon)")
    for champ in ALIAS:
        p.add_argument(f"--crm-{champ.replace('_', '-')}", help=f"force la colonne « {champ} » de l'export CRM")
    a = p.parse_args()

    ent_f, fichier = lire_csv(a.fichier)
    ent_c, crm = lire_csv(a.crm)

    if a.id_fichier not in ent_f:
        sys.exit(f"Colonne « {a.id_fichier} » absente du fichier. En-têtes : {', '.join(ent_f)}")

    col_f = {c: trouver_colonne(ent_f, c) for c in ("siret", "telephone", "site", "nom", "code_postal")}
    col_c = {c: trouver_colonne(ent_c, c, getattr(a, f"crm_{c}")) for c in ALIAS}

    cles_dispo = [c for c in ("siret", "telephone", "site") if col_c[c] and col_f[c]]
    nom_dispo = bool(col_c["nom"] and col_c["code_postal"] and col_f["nom"] and col_f["code_postal"])
    if not cles_dispo and not nom_dispo:
        sys.exit(
            "Aucune clé commune entre le fichier et l'export CRM.\n"
            f"En-têtes du CRM : {', '.join(ent_c)}\n"
            "Réexporte avec au moins le téléphone, ou force une colonne avec --crm-telephone."
        )

    # Un domaine partagé par plusieurs établissements du fichier est celui d'un
    # réseau (la page de l'enseigne), pas celui de l'établissement : il ne peut
    # pas servir de clé.
    domaines_f = Counter(norm_domaine(l.get(col_f["site"], "")) for l in fichier) if col_f["site"] else Counter()
    domaines_c = Counter(norm_domaine(l.get(col_c["site"], "")) for l in crm) if col_c["site"] else Counter()

    index = {"siret": {}, "telephone": {}, "site": {}, "nom": {}}
    for ligne in crm:
        if col_c["siret"]:
            k = norm_siret(ligne.get(col_c["siret"], ""))
            if k:
                index["siret"].setdefault(k, ligne)
        if col_c["telephone"]:
            k = norm_telephone(ligne.get(col_c["telephone"], ""), a.indicatif)
            if k:
                index["telephone"].setdefault(k, ligne)
        if col_c["site"]:
            k = norm_domaine(ligne.get(col_c["site"], ""))
            if k and domaines_c[k] == 1:
                index["site"].setdefault(k, ligne)
        if nom_dispo:
            n, cp = norm_nom(ligne.get(col_c["nom"], "")), norm_cp(ligne.get(col_c["code_postal"], ""))
            if n and cp:
                index["nom"].setdefault((n, cp), ligne)

    libelle = {"siret": "SIRET", "telephone": "Téléphone", "site": "Domaine du site", "nom": "Nom + code postal"}
    compte = Counter()
    sorties = []
    for ligne in fichier:
        trouve, cle = None, ""
        if "siret" in cles_dispo:
            trouve = index["siret"].get(norm_siret(ligne.get(col_f["siret"], "")))
            cle = "siret" if trouve else ""
        if not trouve and "telephone" in cles_dispo:
            trouve = index["telephone"].get(norm_telephone(ligne.get(col_f["telephone"], ""), a.indicatif))
            cle = "telephone" if trouve else ""
        if not trouve and "site" in cles_dispo:
            d = norm_domaine(ligne.get(col_f["site"], ""))
            if d and domaines_f[d] == 1:
                trouve = index["site"].get(d)
                cle = "site" if trouve else ""
        if not trouve and nom_dispo:
            n, cp = norm_nom(ligne.get(col_f["nom"], "")), norm_cp(ligne.get(col_f["code_postal"], ""))
            if n and cp:
                trouve = index["nom"].get((n, cp))
                cle = "nom" if trouve else ""

        if not trouve:
            verdict = "non"
        elif cle == "nom":
            verdict = "à vérifier"
        else:
            verdict = "oui"
        compte[(verdict, cle)] += 1
        sorties.append({
            a.id_fichier: ligne.get(a.id_fichier, ""),
            "Dans le CRM": verdict,
            "Clé de rapprochement": libelle.get(cle, ""),
            "ID CRM": (trouve or {}).get(col_c["id"], "") if col_c["id"] else "",
            "Propriétaire CRM": (trouve or {}).get(col_c["proprietaire"], "") if col_c["proprietaire"] else "",
            "Nom dans le CRM": (trouve or {}).get(col_c["nom"], "") if col_c["nom"] else "",
        })

    sortie = Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    with open(sortie / "rapprochement.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sorties[0].keys()))
        w.writeheader()
        w.writerows(sorties)

    total = len(fichier)
    oui = sum(v for (verdict, _), v in compte.items() if verdict == "oui")
    averif = sum(v for (verdict, _), v in compte.items() if verdict == "à vérifier")
    non = compte[("non", "")]
    pct = lambda n: f"{100 * n / total:.1f} %" if total else "0 %"

    lignes = [
        "Rapprochement fichier / CRM",
        "",
        f"Établissements dans le fichier : {total}",
        f"Lignes dans l'export CRM       : {len(crm)}",
        "",
        f"Déjà dans le CRM     : {oui} ({pct(oui)})",
    ]
    for cle in ("siret", "telephone", "site"):
        if compte[("oui", cle)]:
            lignes.append(f"    par {libelle[cle]:<17}: {compte[('oui', cle)]}")
    lignes += [
        f"À vérifier à la main : {averif} ({pct(averif)})  même nom et même code postal, aucune clé forte",
        f"Absents du CRM       : {non} ({pct(non)})",
        "",
        "Colonnes utilisées",
    ]
    for c in ("siret", "telephone", "site", "nom", "code_postal", "id", "proprietaire"):
        lignes.append(f"    {c:<13}: fichier « {col_f.get(c) or '-'} » · CRM « {col_c.get(c) or 'absente'} »")
    manquantes = [libelle[c] for c in ("siret", "telephone", "site") if c not in cles_dispo]
    if manquantes:
        lignes += ["", "Clés non utilisées, faute de colonne dans l'export CRM : " + ", ".join(manquantes)]
    if not nom_dispo:
        lignes += ["Nom + code postal non utilisé : il manque le nom ou le code postal d'un côté."]
    rapport = "\n".join(lignes) + "\n"
    (sortie / "rapport.txt").write_text(rapport, encoding="utf-8")
    print(rapport)
    print(f"Détail ligne par ligne : {sortie / 'rapprochement.csv'}")


if __name__ == "__main__":
    main()
