"""First-Order Predicate Logic (FOL) structures, ground atoms, unification,
and proof tree generation.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
import json


@dataclass(frozen=True)
class GroundAtom:
    """Represents a ground atomic formula in First-Order Logic (e.g., CreditPrime(applicant_1))."""
    predicate: str
    args: tuple
    value: Any = True

    def __str__(self) -> str:
        args_str = ", ".join(str(a) for a in self.args)
        if self.value is True:
            return f"{self.predicate}({args_str})"
        return f"{self.predicate}({args_str}) = {self.value}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "predicate": self.predicate,
            "args": list(self.args),
            "value": self.value,
            "display": str(self),
        }


@dataclass
class ProofNode:
    """A node in the derivation (proof) tree representing an inference step."""
    conclusion: GroundAtom
    rule_id: Optional[str] = None
    rule_name: Optional[str] = None
    fol_form: Optional[str] = None
    plain_english: Optional[str] = None
    premise_atoms: List[GroundAtom] = field(default_factory=list)
    children: List['ProofNode'] = field(default_factory=list)
    is_leaf: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conclusion": self.conclusion.to_dict(),
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "fol_form": self.fol_form,
            "plain_english": self.plain_english,
            "premise_atoms": [p.to_dict() for p in self.premise_atoms],
            "is_leaf": self.is_leaf,
            "children": [c.to_dict() for c in self.children],
        }


class FOLProofTreeBuilder:
    """Maintains proven atoms and their derivation lineages to construct
    full proof trees for any target conclusion.
    """
    def __init__(self, applicant_id: str = "applicant_1"):
        self.applicant_id = applicant_id
        # Maps predicate or str(GroundAtom) to its ProofNode
        self.proven_nodes: Dict[str, ProofNode] = {}
        self.ground_input_nodes: Dict[str, ProofNode] = {}

    def add_ground_fact(self, atom: GroundAtom, description: str = "Input Fact") -> ProofNode:
        node = ProofNode(
            conclusion=atom,
            rule_id="GROUND_FACT",
            rule_name=description,
            fol_form=str(atom),
            plain_english=f"Observed applicant attribute: {atom}",
            is_leaf=True,
        )
        key = self._key(atom)
        self.ground_input_nodes[key] = node
        self.proven_nodes[key] = node
        return node

    def add_derivation(
        self,
        conclusion: GroundAtom,
        rule_id: str,
        rule_name: str,
        fol_form: str,
        plain_english: str,
        premise_atoms: List[GroundAtom],
    ) -> ProofNode:
        children = []
        for p in premise_atoms:
            pkey = self._key(p)
            if pkey in self.proven_nodes:
                children.append(self.proven_nodes[pkey])
            else:
                # If premise was a ground fact or implicit NAF
                children.append(ProofNode(
                    conclusion=p,
                    rule_id="PREMISE",
                    rule_name="Satisfied Premise",
                    fol_form=str(p),
                    plain_english=f"Ground atom {p} satisfied in working memory",
                    is_leaf=True,
                ))

        node = ProofNode(
            conclusion=conclusion,
            rule_id=rule_id,
            rule_name=rule_name,
            fol_form=fol_form,
            plain_english=plain_english,
            premise_atoms=premise_atoms,
            children=children,
            is_leaf=False,
        )
        self.proven_nodes[self._key(conclusion)] = node
        return node

    def get_tree_for_atom(self, atom: GroundAtom) -> Optional[ProofNode]:
        return self.proven_nodes.get(self._key(atom))

    def get_all_trees(self) -> List[Dict[str, Any]]:
        # Returns all root-level derivation conclusions
        roots = []
        for node in self.proven_nodes.values():
            if not node.is_leaf:
                roots.append(node.to_dict())
        return roots

    def _key(self, atom: GroundAtom) -> str:
        return f"{atom.predicate}:{','.join(str(a) for a in atom.args)}"


def unify_variable(var_name: str, value: Any, substitution: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Unification helper for variable substitution."""
    sub = dict(substitution)
    if var_name in sub:
        if sub[var_name] == value:
            return sub
        return None
    sub[var_name] = value
    return sub
