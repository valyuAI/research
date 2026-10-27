import MinorCore

set_option Elab.async false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

noncomputable section
namespace ValyuResearch.ElasticityMinorCertificates

def original_minor_2_0 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 1, 2])

theorem original_minor_2_0_value (w : Fin 8 → ℂ) :
    original_minor_2_0 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 4)) (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 5))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 5)) (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 5)) (w 7))) (cadd (cmul (-8 : ℂ) (cpow (w 2) 3)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 5)) (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 4) 2))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cmul (cmul (144 : ℂ) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_0
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_1 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 1, 3])

theorem original_minor_2_1_value (w : Fin 8 → ℂ) :
    original_minor_2_1 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 3)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cadd (cmul (cmul (56 : ℂ) (cpow (w 0) 2)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 1)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 3)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 5)) (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (120 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (24 : ℂ) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-72 : ℂ) (cpow (w 7) 3))))))) := by
  unfold original_minor_2_1
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_2 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 1, 4])

theorem original_minor_2_2_value (w : Fin 8 → ℂ) :
    original_minor_2_2 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (96 : ℂ) (w 0)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (-48 : ℂ) (w 4)) (cpow (w 7) 2)) (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2)))))) := by
  unfold original_minor_2_2
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_3 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 1, 6])

theorem original_minor_2_3_value (w : Fin 8 → ℂ) :
    original_minor_2_3 w =
    (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-144 : ℂ) (cpow (w 7) 3))))) := by
  unfold original_minor_2_3
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_4 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 1, 7])

theorem original_minor_2_4_value (w : Fin 8 → ℂ) :
    original_minor_2_4 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 2)) (w 7))) (cadd (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)) (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 5)) (w 7))) (cadd (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 3)) (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_4
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_5 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 1, 9])

theorem original_minor_2_5_value (w : Fin 8 → ℂ) :
    original_minor_2_5 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 3)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (cadd (cmul (cmul (72 : ℂ) (cpow (w 0) 2)) (w 7)) (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 1)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 4))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (cadd (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 3)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 5)) (cmul (cmul (cmul (216 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cadd (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 2)) (w 4)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2))) (cadd (cmul (cmul (24 : ℂ) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)) (cmul (-216 : ℂ) (cpow (w 7) 3))))))) := by
  unfold original_minor_2_5
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_6 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 1, 11])

theorem original_minor_2_6_value (w : Fin 8 → ℂ) :
    original_minor_2_6 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 3)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 3)) (w 7))) (cadd (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (48 : ℂ) (w 1)) (cpow (w 7) 2)) (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (-144 : ℂ) (w 3)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) (w 4)) (w 5)) (w 7))))))) := by
  unfold original_minor_2_6
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_7 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 2, 3])

theorem original_minor_2_7_value (w : Fin 8 → ℂ) :
    original_minor_2_7 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 2)) (w 5))) (cadd (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 5))) (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 5) 2)))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 3)) (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 6))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (-72 : ℂ) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7))))))) := by
  unfold original_minor_2_7
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_8 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 2, 4])

theorem original_minor_2_8_value (w : Fin 8 → ℂ) :
    original_minor_2_8 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 4)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 2)))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 5)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 4)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)))) (cadd (cmul (8 : ℂ) (cpow (w 2) 3)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cmul (cmul (24 : ℂ) (cpow (w 2) 2)) (w 5))))) (cadd (cadd (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 5) 2)))) (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (-48 : ℂ) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_8
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_9 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 2, 6])

theorem original_minor_2_9_value (w : Fin 8 → ℂ) :
    original_minor_2_9 w =
    (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 7))))) := by
  unfold original_minor_2_9
  simp only [Matrix.det_fin_three]
  minor_ring

#eval do
  IO.println "Processed rank-2 minor evaluations 10/70"
  (← IO.getStdout).flush

def original_minor_2_10 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 2, 7])

theorem original_minor_2_10_value (w : Fin 8 → ℂ) :
    original_minor_2_10 w =
    (cadd (cadd (cmul (8 : ℂ) (cpow (w 2) 3)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 5)))) (cadd (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 5) 2))))) := by
  unfold original_minor_2_10
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_11 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 2, 9])

theorem original_minor_2_11_value (w : Fin 8 → ℂ) :
    original_minor_2_11 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 2) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 4))) (cadd (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 2)) (w 5)) (cadd (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 4)) (w 5))))) (cadd (cadd (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 5)) (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 5) 2)) (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 3))) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (-72 : ℂ) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7))))))) := by
  unfold original_minor_2_11
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_12 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 2, 11])

theorem original_minor_2_12_value (w : Fin 8 → ℂ) :
    original_minor_2_12 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 2)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 4) 2))) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 1)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (-48 : ℂ) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)) (cmul (cmul (96 : ℂ) (cpow (w 5) 2)) (w 7))))))) := by
  unfold original_minor_2_12
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_13 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 3, 4])

theorem original_minor_2_13_value (w : Fin 8 → ℂ) :
    original_minor_2_13 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 3)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)))) (cadd (cadd (cmul (cmul (-40 : ℂ) (cpow (w 0) 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 3)) (w 7)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)))) (cadd (cadd (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 4)) (w 5)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 6)) (w 7)) (cmul (cmul (cmul (-56 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (24 : ℂ) (w 3)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)) (cmul (cmul (-24 : ℂ) (cpow (w 4) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)) (cmul (cmul (48 : ℂ) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (-24 : ℂ) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (24 : ℂ) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_13
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_14 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 3, 6])

theorem original_minor_2_14_value (w : Fin 8 → ℂ) :
    original_minor_2_14 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 6)) (w 7)) (cmul (cmul (-48 : ℂ) (w 4)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2)))))) := by
  unfold original_minor_2_14
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_16 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 3, 9])

theorem original_minor_2_16_value (w : Fin 8 → ℂ) :
    original_minor_2_16 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 4)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 3)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) (w 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 6)) (w 7)))) (cadd (cmul (cmul (-48 : ℂ) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_16
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_17 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 3, 11])

theorem original_minor_2_17_value (w : Fin 8 → ℂ) :
    original_minor_2_17 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 4)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (w 5)) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 3)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 4)) (w 7)))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 3)) (w 7)) (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 6)) (w 7)) (cadd (cmul (cmul (-16 : ℂ) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (-48 : ℂ) (w 4)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (-48 : ℂ) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_17
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_18 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 4, 6])

theorem original_minor_2_18_value (w : Fin 8 → ℂ) :
    original_minor_2_18 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cmul (cmul (-24 : ℂ) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-48 : ℂ) (cpow (w 7) 3))))) := by
  unfold original_minor_2_18
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_19 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 4, 7])

theorem original_minor_2_19_value (w : Fin 8 → ℂ) :
    original_minor_2_19 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 4)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 4)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 5)) (w 7)))) (cadd (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 3)) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 4)) (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 4)) (w 5)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 5) 2)))) (cadd (cadd (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 5)) (cpow (w 7) 2))))))) := by
  unfold original_minor_2_19
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_20 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3] ![0, 4, 9])

theorem original_minor_2_20_value (w : Fin 8 → ℂ) :
    original_minor_2_20 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 3)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (cmul (cmul (56 : ℂ) (cpow (w 0) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 1)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 4)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 3)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 4)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 6)) (w 7)) (cmul (cmul (cmul (120 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2))) (cadd (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 2)) (w 4)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (-72 : ℂ) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) (w 3)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)) (cmul (cmul (24 : ℂ) (cpow (w 4) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)) (cmul (cmul (-48 : ℂ) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-72 : ℂ) (cpow (w 7) 3))))))) := by
  unfold original_minor_2_20
  simp only [Matrix.det_fin_three]
  minor_ring

#eval do
  IO.println "Processed rank-2 minor evaluations 20/70"
  (← IO.getStdout).flush


end ValyuResearch.ElasticityMinorCertificates
