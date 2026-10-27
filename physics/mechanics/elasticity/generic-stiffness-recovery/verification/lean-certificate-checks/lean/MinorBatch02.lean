import MinorBatch01

set_option Elab.async false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

noncomputable section
namespace ValyuResearch.ElasticityMinorCertificates

def original_minor_2_22 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![1, 2, 4])

theorem original_minor_2_22_value (w : Fin 8 → ℂ) :
    original_minor_2_22 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 2)) (w 5)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 5) 2)))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 2)) (w 4)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (-64 : ℂ) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7)))))) := by
  unfold original_minor_2_22
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_25 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![2, 3, 6])

theorem original_minor_2_25_value (w : Fin 8 → ℂ) :
    original_minor_2_25 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (32 : ℂ) (w 4)) (w 5)) (w 7)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7)))))) := by
  unfold original_minor_2_25
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_26 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![2, 3, 7])

theorem original_minor_2_26_value (w : Fin 8 → ℂ) :
    original_minor_2_26 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 5))) (cadd (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)))) (cadd (cadd (cmul (cmul (-16 : ℂ) (w 2)) (cpow (w 5) 2)) (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 3))) (cadd (cmul (cmul (24 : ℂ) (cpow (w 4) 2)) (w 5)) (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (cpow (w 5) 2)) (cmul (-8 : ℂ) (cpow (w 5) 3)))))) := by
  unfold original_minor_2_26
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_28 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![3, 4, 6])

theorem original_minor_2_28_value (w : Fin 8 → ℂ) :
    original_minor_2_28 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 7))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 6) 3))) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-16 : ℂ) (cpow (w 7) 3))))) := by
  unfold original_minor_2_28
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_29 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![3, 4, 9])

theorem original_minor_2_29_value (w : Fin 8 → ℂ) :
    original_minor_2_29 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 3)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)))) (cadd (cadd (cmul (cmul (40 : ℂ) (cpow (w 0) 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 4)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 3)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 4)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (64 : ℂ) (w 0)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (56 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (-16 : ℂ) (w 3)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (cmul (cmul (-16 : ℂ) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (24 : ℂ) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-24 : ℂ) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_29
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_30 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 1, 2])

theorem original_minor_2_30_value (w : Fin 8 → ℂ) :
    original_minor_2_30 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 1)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 3)) (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7)) (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 1) 2))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 3)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 6))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-80 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 2) 2))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)) (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 3)) (w 7)))) (cadd (cadd (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 6)) (w 7))) (cadd (cmul (cmul (192 : ℂ) (w 0)) (cpow (w 7) 2)) (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 1) 2)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 2) 2)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 3)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 6)) (w 7)) (cmul (cmul (96 : ℂ) (w 1)) (cpow (w 7) 2))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 3)) (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 6))))) (cadd (cadd (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-56 : ℂ) (w 2)) (w 4)) (w 7)))) (cadd (cadd (cmul (cmul (-144 : ℂ) (w 3)) (cpow (w 7) 2)) (cmul (cmul (cmul (-24 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7))) (cadd (cmul (cmul (-144 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (288 : ℂ) Complex.I) (cpow (w 7) 3))))))) := by
  unfold original_minor_2_30
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_31 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 1, 3])

theorem original_minor_2_31_value (w : Fin 8 → ℂ) :
    original_minor_2_31 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 4)) (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 3))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (64 : ℂ) (w 0)) (w 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (192 : ℂ) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 2)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-48 : ℂ) (w 1)) (w 5)) (w 7)) (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 3)))) (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 4)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5))) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 3)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (120 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (w 4)) (w 7)) (cmul (8 : ℂ) (cpow (w 4) 3)))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (-120 : ℂ) (w 4)) (cpow (w 7) 2)) (cmul (cmul (cmul (288 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_31
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_32 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 1, 4])

theorem original_minor_2_32_value (w : Fin 8 → ℂ) :
    original_minor_2_32 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (48 : ℂ) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)))))) := by
  unfold original_minor_2_32
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_33 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 1, 5])

theorem original_minor_2_33_value (w : Fin 8 → ℂ) :
    original_minor_2_33 w =
    (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 6)) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7)) (cmul (cmul (cmul (-4 : ℂ) (w 0)) (w 1)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 6)) (w 7))) (cadd (cmul (cmul (96 : ℂ) (w 0)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-12 : ℂ) Complex.I) (w 1)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (-24 : ℂ) (w 1)) (cpow (w 7) 2)) (cadd (cmul (cmul (4 : ℂ) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (4 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 7))) (cadd (cmul (cmul (-72 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (144 : ℂ) Complex.I) (cpow (w 7) 3)))))) := by
  unfold original_minor_2_33
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_34 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 1, 6])

theorem original_minor_2_34_value (w : Fin 8 → ℂ) :
    original_minor_2_34 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 4)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 4)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (112 : ℂ) (w 0)) (w 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (112 : ℂ) Complex.I) (w 0)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (96 : ℂ) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 2)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 5)) (w 7)) (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 3)))) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 4)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (192 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (-192 : ℂ) (w 4)) (cpow (w 7) 2)) (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_34
  simp only [Matrix.det_fin_three]
  minor_ring

#eval do
  IO.println "Processed rank-2 minor evaluations 30/70"
  (← IO.getStdout).flush

def original_minor_2_35 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 1, 7])

theorem original_minor_2_35_value (w : Fin 8 → ℂ) :
    original_minor_2_35 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3))) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cmul (cmul (-32 : ℂ) (cpow (w 0) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 3))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (cmul (cmul (cmul (-80 : ℂ) (w 0)) (w 1)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (40 : ℂ) (w 0)) (w 2)) (w 4))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (96 : ℂ) (w 0)) (w 3)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (96 : ℂ) (w 0)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-192 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cmul (cmul (24 : ℂ) (cpow (w 1) 2)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 4))) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 3)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cmul (cmul (56 : ℂ) (cpow (w 2) 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (104 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)) (cmul (cmul (-48 : ℂ) (cpow (w 4) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (288 : ℂ) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_35
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_36 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 1, 9])

theorem original_minor_2_36_value (w : Fin 8 → ℂ) :
    original_minor_2_36 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 4))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 4)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 3))))) (cadd (cadd (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 4))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 2)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 3)) (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 4))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 3)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2))))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (w 4)) (w 7)))) (cadd (cmul (8 : ℂ) (cpow (w 4) 3)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5)) (cmul (cmul (-72 : ℂ) (w 4)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_36
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_37 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 2, 3])

theorem original_minor_2_37_value (w : Fin 8 → ℂ) :
    original_minor_2_37 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 5)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 2)) (w 3)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 3)) (w 4))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 3)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 4)) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 3))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 3)) (w 4)))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 5)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 1)) (w 4)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 5)) (w 7))) (cadd (cmul (16 : ℂ) (cpow (w 2) 3)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 5))))) (cadd (cadd (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 3) 2)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 7)) (cadd (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 6)) (w 7))) (cadd (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 3)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 3)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 5)) (cmul (cmul (cmul (48 : ℂ) (w 4)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (-96 : ℂ) (w 5)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_2_37
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_38 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 2, 4])

theorem original_minor_2_38_value (w : Fin 8 → ℂ) :
    original_minor_2_38 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 1)) (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 3))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 6)) (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7)) (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 1) 2))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 3)) (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cadd (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (w 3)) (w 7))) (cadd (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 4) 2)) (cadd (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (-128 : ℂ) (w 0)) (cpow (w 7) 2)) (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 6))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 7)) (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 2) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 2)) (w 5)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 3)) (w 7)) (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (40 : ℂ) Complex.I) (w 1)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (-32 : ℂ) (w 1)) (cpow (w 7) 2)) (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 3))) (cadd (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 3)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (48 : ℂ) (w 3)) (cpow (w 7) 2)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)))) (cadd (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (-48 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (-96 : ℂ) Complex.I) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_38
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_39 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 2, 5])

theorem original_minor_2_39_value (w : Fin 8 → ℂ) :
    original_minor_2_39 w =
    (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 7))) (cadd (cmul (cmul (cmul (-4 : ℂ) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)))) := by
  unfold original_minor_2_39
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_40 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 2, 6])

theorem original_minor_2_40_value (w : Fin 8 → ℂ) :
    original_minor_2_40 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 2)) (w 7)) (cmul (16 : ℂ) (cpow (w 2) 3)))) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (w 7)) (cadd (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)))) (cadd (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 6)) (w 7)) (cmul (cmul (-32 : ℂ) (w 2)) (cpow (w 7) 2)))))) := by
  unfold original_minor_2_40
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_41 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 2, 7])

theorem original_minor_2_41_value (w : Fin 8 → ℂ) :
    original_minor_2_41 w =
    (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 2) 2)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 5)))) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 3)) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)))))) := by
  unfold original_minor_2_41
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_42 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 2, 9])

theorem original_minor_2_42_value (w : Fin 8 → ℂ) :
    original_minor_2_42 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 5)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 2)) (w 3)) (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 3)) (w 4))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 3)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 4)) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 3))))) (cadd (cadd (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 1)) (w 2)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 3)) (w 4))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 5)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 1)) (w 4)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 5)) (w 7))) (cadd (cmul (-16 : ℂ) (cpow (w 2) 3)) (cadd (cmul (cmul (cmul (-40 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 5))))) (cadd (cadd (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 3) 2)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-88 : ℂ) Complex.I) (w 2)) (w 3)) (w 7)) (cadd (cmul (cmul (32 : ℂ) (w 2)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 2)) (w 6)) (w 7)) (cmul (cmul (-144 : ℂ) (w 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (48 : ℂ) (w 3)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (w 5)) (w 7)) (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 3))))) (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 5)) (cmul (cmul (cmul (48 : ℂ) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (-96 : ℂ) (w 5)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_2_42
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_44 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 3, 5])

theorem original_minor_2_44_value (w : Fin 8 → ℂ) :
    original_minor_2_44 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-4 : ℂ) (w 0)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-4 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 4)) (w 7)) (cmul (cmul (cmul (-4 : ℂ) (w 1)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)) (cmul (cmul (cmul (-4 : ℂ) (w 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 7)) (cadd (cmul (cmul (-4 : ℂ) (w 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (4 : ℂ) Complex.I) (w 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (-24 : ℂ) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (48 : ℂ) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_44
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_45 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 3, 7])

theorem original_minor_2_45_value (w : Fin 8 → ℂ) :
    original_minor_2_45 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 3)) (w 4)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 3)) (w 5)))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 5)) (w 7)) (cmul (cmul (8 : ℂ) (cpow (w 1) 2)) (w 4))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 3)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 3)) (w 4)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 3)) (w 5)))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 5)) (w 6))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 1)) (w 5)) (w 7)) (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 2) 3))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 4)) (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (cpow (w 3) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 7)) (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2)))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (cpow (w 6) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 3)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 3)) (w 5)) (w 7)) (cmul (-16 : ℂ) (cpow (w 4) 3))))) (cadd (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5)) (cadd (cmul (cmul (8 : ℂ) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 4)) (w 6)) (w 7)))) (cadd (cmul (cmul (96 : ℂ) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_2_45
  simp only [Matrix.det_fin_three]
  minor_ring

#eval do
  IO.println "Processed rank-2 minor evaluations 40/70"
  (← IO.getStdout).flush


end ValyuResearch.ElasticityMinorCertificates
