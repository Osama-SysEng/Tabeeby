"""Safe molecular-analysis contract with optional RDKit integration.

This produces cheminformatics descriptors only; it is not a drug safety or
clinical efficacy claim and never recommends a compound for a patient.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MoleculeAnalysis:
    status: str
    canonical_smiles: str | None
    descriptors: dict[str, float]
    clinical_decision: bool = False


def analyze_smiles(smiles: str) -> MoleculeAnalysis:
    if not isinstance(smiles, str) or not 1 <= len(smiles) <= 2000:
        raise ValueError("SMILES must be bounded text")
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors
    except ImportError:
        return MoleculeAnalysis("rdkit_not_installed", None, {}, False)
    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError("invalid SMILES")
    return MoleculeAnalysis(
        "descriptors_only",
        Chem.MolToSmiles(molecule, canonical=True),
        {"molecular_weight": float(Descriptors.MolWt(molecule)), "logp": float(Descriptors.MolLogP(molecule)), "hbd": float(Descriptors.NumHDonors(molecule)), "hba": float(Descriptors.NumHAcceptors(molecule))},
        False,
    )
