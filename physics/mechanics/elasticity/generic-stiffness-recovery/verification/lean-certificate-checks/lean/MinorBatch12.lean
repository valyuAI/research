import MinorBatch11

set_option Elab.async false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

noncomputable section
namespace ValyuResearch.ElasticityMinorCertificates

def original_minor_3_163 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 1, 5, 6])

theorem original_minor_3_163_value (w : Fin 8 → ℂ) :
    original_minor_3_163 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 4)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (cpow (w 0) 2)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (112 : ℂ) (w 0)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (cmul (cmul (112 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (192 : ℂ) Complex.I) (w 0)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 2)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 1)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 3)) (w 6)))) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (192 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (-192 : ℂ) (w 4)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (-288 : ℂ) (w 5)) (cpow (w 7) 3))))))) := by
  unfold original_minor_3_163
  simp only [det_fin_four]
  minor_ring

#eval do
  IO.println "Processed rank-3 minor evaluations 130/167"
  (← IO.getStdout).flush

def original_minor_3_164 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 1, 5, 7])

theorem original_minor_3_164_value (w : Fin 8 → ℂ) :
    original_minor_3_164 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-32 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-80 : ℂ) (w 0)) (w 1)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (40 : ℂ) (w 0)) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (96 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (96 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-192 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (24 : ℂ) (cpow (w 1) 2)) (w 6)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (56 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 4)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (104 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-48 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (144 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (288 : ℂ) (w 6)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_164
  simp only [det_fin_four]
  minor_ring

def original_minor_3_165 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 1, 5, 9])

theorem original_minor_3_165_value (w : Fin 8 → ℂ) :
    original_minor_3_165 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 3)) (w 6)) (cmul (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (w 4)) (w 6)) (w 7)))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 4) 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-72 : ℂ) (w 4)) (w 6)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_165
  simp only [det_fin_four]
  minor_ring

def original_minor_3_166 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 3, 5])

theorem original_minor_3_166_value (w : Fin 8 → ℂ) :
    original_minor_3_166 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 2)) (w 3)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 2)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 4)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 1) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 3)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 3)) (w 4)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 4)) (w 6)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 3) 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 3)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 6) 3)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) (w 3)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 3)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 3)) (w 6)) (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-48 : ℂ) (w 4)) (cpow (w 6) 2)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (96 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_3_166
  simp only [det_fin_four]
  minor_ring

def original_minor_3_167 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 3, 6])

theorem original_minor_3_167_value (w : Fin 8 → ℂ) :
    original_minor_3_167 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (w 5)) (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 1)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 3)) (w 4)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 3)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-64 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 1) 2)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 1) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 2)) (w 3)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 3)) (w 4)) (w 5)))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 3)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-64 : ℂ) (w 1)) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 3)) (w 5)) (cadd (cmul (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 4)) (w 5)) (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 3) 2)) (w 5)) (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 3)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (cpow (w 4) 2)) (w 5)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 4)) (cpow (w 5) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 3)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (96 : ℂ) (w 3)) (cpow (w 5) 2)) (w 7))))) (cadd (cadd (cmul (cmul (-16 : ℂ) (cpow (w 4) 3)) (w 5)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (192 : ℂ) (w 4)) (w 5)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (96 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-192 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_3_167
  simp only [det_fin_four]
  minor_ring

def original_minor_3_168 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 4, 5])

theorem original_minor_3_168_value (w : Fin 8 → ℂ) :
    original_minor_3_168 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 1)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 1) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 3)) (w 6)) (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 1)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 6) 3)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (128 : ℂ) (w 0)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (8 : ℂ) (cpow (w 1) 2)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 3)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 6) 3)) (cmul (cmul (cmul (cmul (-40 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (24 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 3)) (cpow (w 6) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (-48 : ℂ) (w 3)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 6) 3)) (w 7)) (cadd (cmul (cmul (48 : ℂ) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 6)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_168
  simp only [det_fin_four]
  minor_ring

def original_minor_3_169 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 4, 6])

theorem original_minor_3_169_value (w : Fin 8 → ℂ) :
    original_minor_3_169 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 5)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (-64 : ℂ) (cpow (w 0) 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) (w 0)) (w 1)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 2)) (w 4)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 3)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (128 : ℂ) (w 0)) (w 3)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 5)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (64 : ℂ) (w 0)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-256 : ℂ) Complex.I) (w 0)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 1) 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 1) 2)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (w 5)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 2)) (w 4)) (w 5))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 3)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 3)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-80 : ℂ) (w 1)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 1)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 3)) (w 4)) (w 5)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 3)) (cpow (w 5) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (64 : ℂ) (w 2)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (cpow (w 5) 2)) (w 6)) (cadd (cmul (cmul (cmul (-64 : ℂ) (w 2)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (cmul (96 : ℂ) (w 3)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 3)) (w 5)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 4) 2)) (w 5)) (w 7)))) (cadd (cmul (cmul (cmul (96 : ℂ) (w 5)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 5)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (192 : ℂ) (w 5)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_169
  simp only [det_fin_four]
  minor_ring

def original_minor_3_170 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 5, 6])

theorem original_minor_3_170_value (w : Fin 8 → ℂ) :
    original_minor_3_170 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 2)) (w 6)) (w 7)) (cmul (cmul (16 : ℂ) (cpow (w 2) 3)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 5)) (w 7)))) (cadd (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 6) 3)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-32 : ℂ) (w 2)) (w 6)) (cpow (w 7) 2)))))) := by
  unfold original_minor_3_170
  simp only [det_fin_four]
  minor_ring

def original_minor_3_171 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 5, 7])

theorem original_minor_3_171_value (w : Fin 8 → ℂ) :
    original_minor_3_171 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 5)) (w 6)))) (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6)) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)))))) := by
  unfold original_minor_3_171
  simp only [det_fin_four]
  minor_ring

def original_minor_3_172 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 5, 8])

theorem original_minor_3_172_value (w : Fin 8 → ℂ) :
    original_minor_3_172 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)) (w 7))) (cadd (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 6) 3)) (cadd (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 6)) (cpow (w 7) 2)))))) (cadd (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 1) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 1) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 3)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 6) 3)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (32 : ℂ) (cpow (w 2) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 7) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 3)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (96 : ℂ) (w 3)) (w 6)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 6) 3)) (w 7)) (cadd (cmul (cmul (192 : ℂ) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (-192 : ℂ) Complex.I) (w 6)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_172
  simp only [det_fin_four]
  minor_ring

def original_minor_3_173 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 4, 6] ![0, 2, 5, 9])

theorem original_minor_3_173_value (w : Fin 8 → ℂ) :
    original_minor_3_173 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (24 : ℂ) (w 0)) (w 1)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 2)) (w 3)) (w 6)) (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 2)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 3)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 3)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 1)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 3)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-32 : ℂ) (w 1)) (w 4)) (w 6)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-40 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 3) 2)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-88 : ℂ) Complex.I) (w 2)) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (32 : ℂ) (w 2)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 2)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-144 : ℂ) (w 2)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) (w 3)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 3)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (48 : ℂ) (w 4)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 5)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_3_173
  simp only [det_fin_four]
  minor_ring

#eval do
  IO.println "Processed rank-3 minor evaluations 140/167"
  (← IO.getStdout).flush

def original_minor_3_174 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 1, 2, 5])

theorem original_minor_3_174_value (w : Fin 8 → ℂ) :
    original_minor_3_174 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (cpow (w 0) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)))) (cadd (cmul (cmul (cmul (48 : ℂ) (w 2)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (144 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2)))))) := by
  unfold original_minor_3_174
  simp only [det_fin_four]
  minor_ring

def original_minor_3_175 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 1, 2, 6])

theorem original_minor_3_175_value (w : Fin 8 → ℂ) :
    original_minor_3_175 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 2)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (-192 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (48 : ℂ) (w 1)) (cpow (w 5) 2)) (w 7)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (cpow (w 5) 2)))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 4)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (-288 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2)))))) := by
  unfold original_minor_3_175
  simp only [det_fin_four]
  minor_ring

def original_minor_3_176 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 1, 3, 5])

theorem original_minor_3_176_value (w : Fin 8 → ℂ) :
    original_minor_3_176 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (104 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (168 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (120 : ℂ) (w 6)) (cpow (w 7) 3))))))) := by
  unfold original_minor_3_176
  simp only [det_fin_four]
  minor_ring

def original_minor_3_177 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 1, 4, 5])

theorem original_minor_3_177_value (w : Fin 8 → ℂ) :
    original_minor_3_177 w =
    (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 4)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 4)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 5)) (w 6)) (cpow (w 7) 2))))) := by
  unfold original_minor_3_177
  simp only [det_fin_four]
  minor_ring

def original_minor_3_178 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 1, 5, 6])

theorem original_minor_3_178_value (w : Fin 8 → ℂ) :
    original_minor_3_178 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 5) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (80 : ℂ) (w 0)) (w 1)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (-192 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-104 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (208 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-24 : ℂ) (cpow (w 1) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (w 6)))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 3)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (48 : ℂ) (w 1)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (24 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-144 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-288 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-168 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (-336 : ℂ) (w 6)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_178
  simp only [det_fin_four]
  minor_ring

def original_minor_3_180 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 1, 5, 9])

theorem original_minor_3_180_value (w : Fin 8 → ℂ) :
    original_minor_3_180 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (-72 : ℂ) (w 6)) (cpow (w 7) 3)))))) := by
  unfold original_minor_3_180
  simp only [det_fin_four]
  minor_ring

def original_minor_3_181 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 1, 5, 11])

theorem original_minor_3_181_value (w : Fin 8 → ℂ) :
    original_minor_3_181 w =
    (cadd (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (112 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) (w 3)) (w 6)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 4)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (-192 : ℂ) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 6)) (cpow (w 7) 3)))))) := by
  unfold original_minor_3_181
  simp only [det_fin_four]
  minor_ring

def original_minor_3_182 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 3, 5])

theorem original_minor_3_182_value (w : Fin 8 → ℂ) :
    original_minor_3_182 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (16 : ℂ) (w 0)) (cpow (w 5) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 1)) (cpow (w 5) 2)) (w 6))) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-56 : ℂ) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (w 7)))))) := by
  unfold original_minor_3_182
  simp only [det_fin_four]
  minor_ring

def original_minor_3_183 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 3, 6])

theorem original_minor_3_183_value (w : Fin 8 → ℂ) :
    original_minor_3_183 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 3)))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 3))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-32 : ℂ) (cpow (w 2) 2)) (w 5)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 5) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 4) 2)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (cmul (112 : ℂ) Complex.I) (w 4)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (96 : ℂ) (cpow (w 5) 3)) (w 7)))))) := by
  unfold original_minor_3_183
  simp only [det_fin_four]
  minor_ring


end ValyuResearch.ElasticityMinorCertificates
