"""Tests for First-Order Predicate Logic structures, unification, and proof trees."""

import pytest
from app.logic.fol import GroundAtom, ProofNode, FOLProofTreeBuilder, unify_variable


def test_ground_atom_representation():
    atom = GroundAtom("CreditPrime", ("applicant_101",))
    assert str(atom) == "CreditPrime(applicant_101)"
    d = atom.to_dict()
    assert d["predicate"] == "CreditPrime"
    assert d["args"] == ["applicant_101"]
    assert d["value"] is True

    atom_val = GroundAtom("CreditScore", ("applicant_101", 780), 780)
    assert atom_val.value == 780


def test_fol_unification():
    sub = {}
    sub = unify_variable("x", "applicant_1", sub)
    assert sub == {"x": "applicant_1"}
    
    # Consistent unification
    sub2 = unify_variable("x", "applicant_1", sub)
    assert sub2 == {"x": "applicant_1"}
    
    # Conflict unification
    sub_fail = unify_variable("x", "applicant_2", sub)
    assert sub_fail is None


def test_proof_tree_construction():
    builder = FOLProofTreeBuilder("app_1")
    
    # Input leaf atoms
    cs_atom = GroundAtom("CreditScore", ("app_1", 780), 780)
    builder.add_ground_fact(cs_atom, "Observed Credit Score")
    
    # Derivation step
    prime_atom = GroundAtom("CreditPrime", ("app_1",))
    builder.add_derivation(
        conclusion=prime_atom,
        rule_id="DER_CS_01",
        rule_name="Derive Prime Credit Score",
        fol_form="forall x: CreditScoreAtLeast(x, 750) -> CreditPrime(x)",
        plain_english="Credit score >= 750 is Prime",
        premise_atoms=[cs_atom],
    )

    # Next layer derivation step
    eligible_atom = GroundAtom("FinalDecision", ("app_1", "ELIGIBLE"))
    builder.add_derivation(
        conclusion=eligible_atom,
        rule_id="DEC_002",
        rule_name="Full Eligibility Rule",
        fol_form="forall x: CreditPrime(x) -> FinalDecision(x, ELIGIBLE)",
        plain_english="Prime applicant is eligible",
        premise_atoms=[prime_atom],
    )

    tree = builder.get_tree_for_atom(eligible_atom)
    assert tree is not None
    assert tree.rule_id == "DEC_002"
    assert len(tree.children) == 1
    assert tree.children[0].rule_id == "DER_CS_01"
    assert len(tree.children[0].children) == 1
    assert tree.children[0].children[0].is_leaf is True
