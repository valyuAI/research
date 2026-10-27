# Understanding the tree reconstruction

The question is whether changing coordinates can make two genuinely different tree-indexed differential-equation families look identical. For generic parameters, the paper proves that it cannot.

1. **The tree controls column equalities.** Removing a vertex splits the tree into components; entries in that vertex's column agree within each component. These equalities define the family.
2. **Look at linear Darboux forms.** These are linear functions whose derivatives equal the functions themselves times another linear function. Invertible changes of variables preserve the full set of these forms.
3. **Prove the set is complete.** Generic column inequalities force each form's support to be connected. A three-vertex path gives an algebraic contradiction if the support has three or more vertices. Only coordinate forms and one two-variable form per tree edge remain.
4. **Forget coordinate labels.** Three of those projective points are dependent precisely when they consist of an edge form and its two endpoints. Those triples are intrinsic to the configuration.
5. **Rebuild the tree from shared points.** A point occurring in two or more triples is an internal vertex. Triples join internal vertices or attach leaves. The one- and two-vertex cases are immediate.

A four-vertex path gives two points each shared by two triples. A four-vertex star gives one point shared by three triples. This is how the invariant distinguishes them even after coordinates are mixed.

Check why the generic assumptions matter: if all matrix rows agree, every linear form is Darboux and the finite configuration disappears. Also explain the provenance honestly: a withdrawn preprint announced a closely matching theorem before this work. Our proof and verification are independently available; first discovery is not claimed.
