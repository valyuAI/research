import MinorBatch09

set_option Elab.async false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

noncomputable section
namespace ValyuResearch.ElasticityMinorCertificates

def original_minor_3_103 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 5] ![0, 3, 4, 11])

theorem original_minor_3_103_value (w : Fin 8 → ℂ) :
    original_minor_3_103 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 3)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-96 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (80 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (-80 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 3)) (cpow (w 7) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 6) 3)) (cadd (cmul (cmul (cmul (-160 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (-80 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (-64 : ℂ) (w 0)) (cpow (w 7) 3)) (cmul (cmul (cmul (64 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (32 : ℂ) (w 1)) (cpow (w 7) 3)) (cmul (cmul (cmul (-64 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (-128 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (-64 : ℂ) (w 2)) (w 4)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (-192 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (-64 : ℂ) (w 3)) (cpow (w 6) 2)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (-32 : ℂ) (w 3)) (cpow (w 7) 3))) (cadd (cmul (cmul (cmul (64 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 4) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (cmul (-192 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-96 : ℂ) (w 4)) (w 5)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-128 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (64 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2)))) (cadd (cmul (cmul (-64 : ℂ) (cpow (w 6) 3)) (w 7)) (cadd (cmul (cmul (cmul (-96 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 7) 4)))))))) := by
  unfold original_minor_3_103
  simp only [det_fin_four]
  minor_ring

#eval do
  IO.println "Processed rank-3 minor evaluations 90/167"
  (← IO.getStdout).flush

def original_minor_3_104 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 5] ![0, 3, 5, 6])

theorem original_minor_3_104_value (w : Fin 8 → ℂ) :
    original_minor_3_104 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (96 : ℂ) (w 4)) (w 5)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (48 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2)))))) := by
  unfold original_minor_3_104
  simp only [det_fin_four]
  minor_ring

def original_minor_3_105 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 5] ![0, 3, 5, 9])

theorem original_minor_3_105_value (w : Fin 8 → ℂ) :
    original_minor_3_105 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 1)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (128 : ℂ) (w 0)) (w 2)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 4)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 6))) (cadd (cmul (cmul (cmul (-64 : ℂ) (w 1)) (cpow (w 5) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-64 : ℂ) (w 2)) (w 3)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (96 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (96 : ℂ) (w 4)) (w 5)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (48 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_105
  simp only [det_fin_four]
  minor_ring

def original_minor_3_106 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 5] ![0, 3, 6, 7])

theorem original_minor_3_106_value (w : Fin 8 → ℂ) :
    original_minor_3_106 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 1)) (cpow (w 2) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)) (w 5)))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (cpow (w 5) 2)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (cpow (w 2) 2)) (w 3))) (cadd (cmul (cmul (cmul (32 : ℂ) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 4)) (w 5)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 3)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (64 : ℂ) (w 0)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (cpow (w 5) 2)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 1) 2)) (w 2)) (w 4)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 1) 2)) (w 2)) (w 5)))) (cadd (cadd (cmul (cmul (-16 : ℂ) (cpow (w 1) 2)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 1) 2)) (w 4)) (w 5))) (cadd (cmul (cmul (16 : ℂ) (cpow (w 1) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (16 : ℂ) (w 1)) (cpow (w 2) 2)) (w 3))))) (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 1)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (-64 : ℂ) (w 1)) (w 2)) (w 4)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (80 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 3)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 3)) (w 4)) (w 5))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 3)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (cpow (w 4) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 1)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (cpow (w 3) 2)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (w 7)) (cmul (cmul (48 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-80 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7)) (cmul (cmul (32 : ℂ) (cpow (w 2) 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (cpow (w 3) 2)) (w 4)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (cpow (w 3) 2)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (96 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-128 : ℂ) (w 2)) (w 5)) (cpow (w 7) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) (w 3)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 3)) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7)) (cmul (cmul (-32 : ℂ) (cpow (w 4) 2)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-128 : ℂ) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (256 : ℂ) Complex.I) (w 4)) (w 5)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (112 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (w 7)) (cmul (cmul (224 : ℂ) (cpow (w 5) 2)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_3_106
  simp only [det_fin_four]
  minor_ring

def original_minor_3_110 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 1, 2, 5])

theorem original_minor_3_110_value (w : Fin 8 → ℂ) :
    original_minor_3_110 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 4)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 2)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 3)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 4) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-144 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_110
  simp only [det_fin_four]
  minor_ring

def original_minor_3_111 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 1, 3, 5])

theorem original_minor_3_111_value (w : Fin 8 → ℂ) :
    original_minor_3_111 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6)))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (-56 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (-48 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-120 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (-24 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-72 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (72 : ℂ) (w 6)) (cpow (w 7) 3))))))) := by
  unfold original_minor_3_111
  simp only [det_fin_four]
  minor_ring

def original_minor_3_112 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 1, 4, 5])

theorem original_minor_3_112_value (w : Fin 8 → ℂ) :
    original_minor_3_112 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) (w 0)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 2)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 4)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 4)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-144 : ℂ) Complex.I) (w 5)) (w 6)) (cpow (w 7) 2)))))) := by
  unfold original_minor_3_112
  simp only [det_fin_four]
  minor_ring

def original_minor_3_113 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 1, 5, 6])

theorem original_minor_3_113_value (w : Fin 8 → ℂ) :
    original_minor_3_113 w =
    (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-72 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (-144 : ℂ) (w 6)) (cpow (w 7) 3))))) := by
  unfold original_minor_3_113
  simp only [det_fin_four]
  minor_ring

def original_minor_3_114 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 1, 5, 7])

theorem original_minor_3_114_value (w : Fin 8 → ℂ) :
    original_minor_3_114 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 2)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 3)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 5)) (w 6)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_114
  simp only [det_fin_four]
  minor_ring

def original_minor_3_115 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 1, 5, 9])

theorem original_minor_3_115_value (w : Fin 8 → ℂ) :
    original_minor_3_115 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 3)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (72 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 1)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (216 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (24 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (-216 : ℂ) (w 6)) (cpow (w 7) 3))))))) := by
  unfold original_minor_3_115
  simp only [det_fin_four]
  minor_ring

def original_minor_3_116 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 2, 3, 5])

theorem original_minor_3_116_value (w : Fin 8 → ℂ) :
    original_minor_3_116 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 5) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 5) 2)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6)) (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (72 : ℂ) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (w 7))))))) := by
  unfold original_minor_3_116
  simp only [det_fin_four]
  minor_ring

#eval do
  IO.println "Processed rank-3 minor evaluations 100/167"
  (← IO.getStdout).flush

def original_minor_3_117 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 2, 4, 5])

theorem original_minor_3_117_value (w : Fin 8 → ℂ) :
    original_minor_3_117 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 2)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 4)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (cpow (w 6) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7)))) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (cpow (w 5) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (24 : ℂ) (w 4)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 5)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (48 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_117
  simp only [det_fin_four]
  minor_ring

def original_minor_3_118 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 2, 5, 6])

theorem original_minor_3_118_value (w : Fin 8 → ℂ) :
    original_minor_3_118 w =
    (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7))))) := by
  unfold original_minor_3_118
  simp only [det_fin_four]
  minor_ring

def original_minor_3_119 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 2, 5, 7])

theorem original_minor_3_119_value (w : Fin 8 → ℂ) :
    original_minor_3_119 w =
    (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6)))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 5) 2)) (w 6))))) := by
  unfold original_minor_3_119
  simp only [det_fin_four]
  minor_ring

def original_minor_3_120 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 2, 5, 9])

theorem original_minor_3_120_value (w : Fin 8 → ℂ) :
    original_minor_3_120 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-72 : ℂ) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (w 7))))))) := by
  unfold original_minor_3_120
  simp only [det_fin_four]
  minor_ring

def original_minor_3_121 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 3, 4, 5])

theorem original_minor_3_121_value (w : Fin 8 → ℂ) :
    original_minor_3_121 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 3)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (40 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 6))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 3)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 6) 3)) (cadd (cmul (cmul (cmul (64 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (56 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 3)) (cmul (cmul (cmul (-16 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 6) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) (w 3)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (24 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (24 : ℂ) (cpow (w 6) 3)) (w 7)) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (-24 : ℂ) (w 6)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_121
  simp only [det_fin_four]
  minor_ring

def original_minor_3_122 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 3, 6] ![0, 3, 5, 9])

theorem original_minor_3_122_value (w : Fin 8 → ℂ) :
    original_minor_3_122 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 5)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 4)) (cpow (w 6) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 3)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) (w 2)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (cpow (w 6) 2)) (w 7)))) (cadd (cmul (cmul (cmul (-48 : ℂ) (w 4)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 5)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (w 6)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_122
  simp only [det_fin_four]
  minor_ring

def original_minor_3_123 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 5] ![0, 1, 2, 3])

theorem original_minor_3_123_value (w : Fin 8 → ℂ) :
    original_minor_3_123 w =
    (cadd (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 1)) (w 7))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 3)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (64 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (80 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 1) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 4)) (w 5)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (160 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 7) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) (w 0)) (w 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-192 : ℂ) (w 0)) (w 2)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 3) 2)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 3)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-224 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (160 : ℂ) Complex.I) (w 0)) (w 3)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-160 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-384 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7)) (cadd (cmul (cmul (cmul (-208 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (544 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2))))) (cadd (cadd (cmul (cmul (256 : ℂ) (w 0)) (cpow (w 7) 3)) (cmul (cmul (cmul (-48 : ℂ) (cpow (w 1) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 1) 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 1)) (cpow (w 2) 2)) (w 7)))))))) (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (64 : ℂ) (w 1)) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) (w 1)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (w 1)) (cpow (w 4) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (96 : ℂ) (w 1)) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (48 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (192 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (144 : ℂ) (w 1)) (cpow (w 7) 3)))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 3)) (w 5)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 3)) (w 7)) (cadd (cmul (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 4)) (w 5)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-48 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 3)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 3)) (w 5)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2)) (w 5)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-112 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-400 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 7) 2))))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 3) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (16 : ℂ) (w 3)) (cpow (w 4) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 3)) (w 4)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-384 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (-336 : ℂ) (w 3)) (cpow (w 7) 3)))))) (cadd (cadd (cadd (cmul (cmul (-16 : ℂ) (cpow (w 4) 3)) (w 5)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (64 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 4) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (304 : ℂ) (w 4)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (-576 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-336 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (-912 : ℂ) (w 6)) (cpow (w 7) 3)) (cmul (cmul (480 : ℂ) Complex.I) (cpow (w 7) 4))))))))) := by
  unfold original_minor_3_123
  simp only [det_fin_four]
  minor_ring

def original_minor_3_124 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 5] ![0, 1, 2, 4])

theorem original_minor_3_124_value (w : Fin 8 → ℂ) :
    original_minor_3_124 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 1)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 3)) (w 5)) (w 7)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (cpow (w 5) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (w 5)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 2)) (cpow (w 7) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 4)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 1)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (cpow (w 2) 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 3)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 3)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 4)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) (w 2)) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (64 : ℂ) (w 2)) (cpow (w 7) 3)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 3)) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 3)) (w 4)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 3)) (w 5)) (cpow (w 7) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (cpow (w 4) 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 4)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 4)) (cpow (w 6) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) (w 4)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 4)) (cpow (w 7) 3))) (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 5)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (192 : ℂ) (w 5)) (cpow (w 7) 3))))))) := by
  unfold original_minor_3_124
  simp only [det_fin_four]
  minor_ring

def original_minor_3_125 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 5] ![0, 1, 2, 5])

theorem original_minor_3_125_value (w : Fin 8 → ℂ) :
    original_minor_3_125 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (cpow (w 0) 2)) (w 1)) (w 5)) (cmul (cmul (cmul (32 : ℂ) (cpow (w 0) 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 1) 2)) (w 5)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-176 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (w 7)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (cpow (w 2) 2)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)) (w 5)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (192 : ℂ) Complex.I) (w 0)) (w 3)) (w 5)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 4) 2)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (192 : ℂ) (w 0)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 1) 2)) (w 5)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 1)) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 1)) (w 3)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (240 : ℂ) (w 1)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (80 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-128 : ℂ) (w 2)) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (48 : ℂ) (w 2)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 2)) (cpow (w 7) 3)) (cmul (cmul (cmul (-288 : ℂ) (w 3)) (w 5)) (cpow (w 7) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (48 : ℂ) (w 4)) (cpow (w 7) 3)) (cadd (cmul (cmul (cmul (-144 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (288 : ℂ) Complex.I) (w 5)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_125
  simp only [det_fin_four]
  minor_ring


end ValyuResearch.ElasticityMinorCertificates
