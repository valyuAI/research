import MinorBatch02

set_option Elab.async false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

noncomputable section
namespace ValyuResearch.ElasticityMinorCertificates

def original_minor_2_46 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![0, 4, 5])

theorem original_minor_2_46_value (w : Fin 8 → ℂ) :
    original_minor_2_46 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7))) (cadd (cmul (cmul (cmul (-4 : ℂ) (w 0)) (w 1)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)))) (cadd (cadd (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 6)) (w 7))) (cadd (cmul (cmul (64 : ℂ) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (-4 : ℂ) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (4 : ℂ) Complex.I) (w 1)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 7) 2)) (cmul (cmul (4 : ℂ) (cpow (w 2) 2)) (w 6))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (4 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (24 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 7) 3))))))) := by
  unfold original_minor_2_46
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_47 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![1, 2, 3])

theorem original_minor_2_47_value (w : Fin 8 → ℂ) :
    original_minor_2_47 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 0) 2)) (w 1)) (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 3))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 6)) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 3))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 2) 2)))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)) (cadd (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 2)) (w 5)) (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 3) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 7))) (cadd (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 6)) (w 7)) (cadd (cmul (cmul (64 : ℂ) (w 0)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 3)) (w 7)) (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 6)) (w 7))) (cadd (cmul (cmul (24 : ℂ) (w 1)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-56 : ℂ) (w 2)) (w 4)) (w 7)))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (80 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 3) 2)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (w 3)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 3)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (24 : ℂ) (w 3)) (cpow (w 7) 2)) (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 4)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (24 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_47
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_48 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![2, 3, 4])

theorem original_minor_2_48_value (w : Fin 8 → ℂ) :
    original_minor_2_48 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 0) 2)) (w 1)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 3)) (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 6)))) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 3)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cadd (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 2)) (w 5)) (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 3) 2))) (cadd (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 3)) (w 6)) (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 4) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (cadd (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 6)) (w 7)))) (cadd (cmul (cmul (32 : ℂ) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 3)) (w 7)) (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (cmul (cmul (-16 : ℂ) (w 1)) (cpow (w 5) 2))) (cadd (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 6)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 7) 2)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 4)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (40 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 3) 2)) (w 6)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 3) 2)) (w 7))) (cadd (cmul (cmul (-8 : ℂ) (w 3)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 3)) (w 4)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (w 3)) (cpow (w 5) 2)) (cadd (cmul (cmul (16 : ℂ) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 3)) (w 6)) (w 7)))) (cadd (cmul (cmul (8 : ℂ) (w 3)) (cpow (w 7) 2)) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (40 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (32 : ℂ) (w 4)) (w 5)) (w 7)) (cmul (cmul (16 : ℂ) (cpow (w 5) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7)) (cmul (8 : ℂ) (cpow (w 6) 3))) (cadd (cmul (cmul (24 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_48
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_49 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4] ![2, 3, 7])

theorem original_minor_2_49_value (w : Fin 8 → ℂ) :
    original_minor_2_49 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 5))) (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (-8 : ℂ) (w 3)) (cpow (w 4) 2))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 3)) (w 4)) (w 5)) (cadd (cmul (cmul (8 : ℂ) (w 3)) (cpow (w 5) 2)) (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (32 : ℂ) (w 4)) (w 5)) (w 7)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7))))))) := by
  unfold original_minor_2_49
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_50 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 1, 2])

theorem original_minor_2_50_value (w : Fin 8 → ℂ) :
    original_minor_2_50 w =
    (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 5))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)))) (cadd (cmul (cmul (-48 : ℂ) (w 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cmul (cmul (-144 : ℂ) (w 5)) (cpow (w 7) 2)))))) := by
  unfold original_minor_2_50
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_51 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 1, 3])

theorem original_minor_2_51_value (w : Fin 8 → ℂ) :
    original_minor_2_51 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 7)) (cmul (cmul (cmul (-104 : ℂ) (w 0)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)) (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (-168 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-120 : ℂ) (cpow (w 7) 3))))))) := by
  unfold original_minor_2_51
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_53 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 1, 5])

theorem original_minor_2_53_value (w : Fin 8 → ℂ) :
    original_minor_2_53 w =
    (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 5)) (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)) (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 5))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (cmul (cmul (-144 : ℂ) (w 5)) (cpow (w 7) 2))))) := by
  unfold original_minor_2_53
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_54 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 1, 6])

theorem original_minor_2_54_value (w : Fin 8 → ℂ) :
    original_minor_2_54 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)))) (cadd (cmul (cmul (32 : ℂ) (cpow (w 0) 2)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 3))))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (cadd (cmul (cmul (cmul (80 : ℂ) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) (w 0)) (w 3)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-104 : ℂ) (w 0)) (w 6)) (w 7)) (cmul (cmul (cmul (208 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2))) (cadd (cmul (cmul (-24 : ℂ) (cpow (w 1) 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 4)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 3)) (w 7)) (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6))))) (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (-144 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-168 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-336 : ℂ) (cpow (w 7) 3))))))) := by
  unfold original_minor_2_54
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_55 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 1, 7])

theorem original_minor_2_55_value (w : Fin 8 → ℂ) :
    original_minor_2_55 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 5))) (cadd (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 7)) (cmul (cmul (cmul (104 : ℂ) (w 0)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 5)))) (cadd (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (-48 : ℂ) (w 4)) (cpow (w 7) 2)) (cmul (cmul (cmul (168 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2)))))) := by
  unfold original_minor_2_55
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_56 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 1, 9])

theorem original_minor_2_56_value (w : Fin 8 → ℂ) :
    original_minor_2_56 w =
    (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 7)))) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)) (cmul (-72 : ℂ) (cpow (w 7) 3)))))) := by
  unfold original_minor_2_56
  simp only [Matrix.det_fin_three]
  minor_ring

#eval do
  IO.println "Processed rank-2 minor evaluations 50/70"
  (← IO.getStdout).flush

def original_minor_2_57 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 1, 11])

theorem original_minor_2_57_value (w : Fin 8 → ℂ) :
    original_minor_2_57 w =
    (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 6)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (112 : ℂ) Complex.I) (w 0)) (w 6)) (w 7)) (cmul (cmul (32 : ℂ) (w 0)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 6)) (w 7)) (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 6))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (-48 : ℂ) (w 3)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (-192 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (96 : ℂ) Complex.I) (cpow (w 7) 3)))))) := by
  unfold original_minor_2_57
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_58 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 2, 3])

theorem original_minor_2_58_value (w : Fin 8 → ℂ) :
    original_minor_2_58 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 2)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 5) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 5) 2))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7))) (cadd (cmul (cmul (cmul (56 : ℂ) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7)))))) := by
  unfold original_minor_2_58
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_59 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 2, 4])

theorem original_minor_2_59_value (w : Fin 8 → ℂ) :
    original_minor_2_59 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 5)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5))) (cadd (cmul (cmul (-16 : ℂ) (w 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (48 : ℂ) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_59
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_61 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 2, 6])

theorem original_minor_2_61_value (w : Fin 8 → ℂ) :
    original_minor_2_61 w =
    (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (w 1)) (cpow (w 2) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 3)) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)))))) := by
  unfold original_minor_2_61
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_62 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 2, 9])

theorem original_minor_2_62_value (w : Fin 8 → ℂ) :
    original_minor_2_62 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 2)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 5) 2)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 5) 2)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-88 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (56 : ℂ) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7)))))) := by
  unfold original_minor_2_62
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_64 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 3, 5])

theorem original_minor_2_64_value (w : Fin 8 → ℂ) :
    original_minor_2_64 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5))) (cadd (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (-48 : ℂ) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7)))))) := by
  unfold original_minor_2_64
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_65 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 3, 6])

theorem original_minor_2_65_value (w : Fin 8 → ℂ) :
    original_minor_2_65 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 7))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 3)) (w 4)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 5))))) (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 4)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 5))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 3)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 4)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (cpow (w 3) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (w 6))))) (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 7)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (w 4)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) (w 3)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-56 : ℂ) Complex.I) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (-112 : ℂ) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-56 : ℂ) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (112 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_2_65
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_67 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 3, 9])

theorem original_minor_2_67_value (w : Fin 8 → ℂ) :
    original_minor_2_67 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 7))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 5)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 3)) (w 7))) (cadd (cmul (cmul (cmul (80 : ℂ) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (56 : ℂ) Complex.I) (w 4)) (w 6)) (w 7)) (cmul (cmul (16 : ℂ) (w 4)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (56 : ℂ) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2)))))) := by
  unfold original_minor_2_67
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_68 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 4, 5])

theorem original_minor_2_68_value (w : Fin 8 → ℂ) :
    original_minor_2_68 w =
    (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 5))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)))) (cadd (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (-48 : ℂ) (w 5)) (cpow (w 7) 2)))))) := by
  unfold original_minor_2_68
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_69 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![0, 4, 6])

theorem original_minor_2_69_value (w : Fin 8 → ℂ) :
    original_minor_2_69 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cmul (cmul (32 : ℂ) (cpow (w 0) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 3))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 3)) (w 7)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (-40 : ℂ) (w 0)) (w 6)) (w 7)) (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 6)) (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 2)) (w 5))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 3)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (40 : ℂ) (w 1)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 4)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2))) (cadd (cmul (cmul (-56 : ℂ) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (56 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-112 : ℂ) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_69
  simp only [Matrix.det_fin_three]
  minor_ring

#eval do
  IO.println "Processed rank-2 minor evaluations 60/70"
  (← IO.getStdout).flush


end ValyuResearch.ElasticityMinorCertificates
