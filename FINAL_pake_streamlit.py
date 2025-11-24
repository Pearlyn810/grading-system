import streamlit as st
from tabulate import tabulate
import time

NIM = []
NAMA = []

ASSIGNMENTS = []
FINAL_ASSIGNMENT = []

QUIZZES = []
FINAL_QUIZ = []

PROJECT = []
MID = []
FINAL = []

GRADE = []
GRADE_LETTER = []

def hitung_nilai_akhir(project, mid, final, nilai_tugas=[], nilai_quiz=[]):
    rata_tugas = sum(nilai_tugas) // len(nilai_tugas) if len(nilai_tugas) > 0 else 0
    rata_quiz = sum(nilai_quiz) // len(nilai_quiz) if len(nilai_quiz) > 0 else 0

    assignment = int(rata_tugas * 0.20)
    quiz = int(rata_quiz * 0.15)
    project_score = int(project * 0.15)
    mid_score = int(mid * 0.25)
    final_score = int(final * 0.25)

    nilai_akhir = assignment + quiz + project_score + mid_score + final_score
    
    #append data ke variable global
    FINAL_ASSIGNMENT.append(assignment)
    FINAL_QUIZ.append(quiz)
    PROJECT.append(project_score)
    MID.append(mid_score)
    FINAL.append(final_score)
    return nilai_akhir

def nilai_huruf(nilai_akhir):
    na = nilai_akhir
    if na >= 91 and na <= 100: return "A"
    elif na >= 85 and na <= 90: return "A-"
    elif na >= 82 and na <= 84: return "B+"
    elif na >= 78 and na <= 81: return "B"
    elif na >= 75 and na <= 77: return "B-"
    elif na >= 70 and na <= 74: return "C+"
    elif na >= 67 and na <= 69: return "C"
    elif na >= 60 and na <= 66: return "C-"
    elif na >= 40 and na <= 59: return "D"
    else: return "F"
    
def tampilkan_nilai_final():
    output_text = "\n=== DAFTAR NILAI MAHASISWA ===\n"
    for i in range(len(NAMA)):
        output_text += f"{i+1}. {NAMA[i]} - {GRADE[i]} ({GRADE_LETTER[i]})\n"
    return output_text
    
def highest_lowest():
    highest = lowest = 0
    for i in range(len(GRADE)):
        if GRADE[i] > GRADE[highest]:
            highest = i
        elif GRADE[i] < GRADE[lowest]:
            lowest = i
    return highest, lowest

def tidak_lulus():
    counter = 0
    text_taklulus = ""
    
    for i in range(len(GRADE)):
        if GRADE[i] < 67: 
            counter += 1
            text_taklulus += f"- {NAMA[i]} (Nilai: {GRADE[i]})\n"
            
    if counter == 0: 
        text_jumlah = None
    else: 
        text_jumlah = f"Jumlah siswa yang tidak lulus: {counter} orang\n"  
    
    return text_jumlah, text_taklulus

def display_report():
    jml_tugas = len(ASSIGNMENTS[0]) 
    jml_quiz = len(QUIZZES[0])

    #header
    header = ["NIM", "NAMA"]
    for k in range(jml_tugas):
        header.append(f"A-{k+1}")
    header.append("Assignment(20%)")
     
    for k in range(jml_quiz):
        header.append(f"Q-{k+1}")
    header.append("Quiz(15%)")
    header += ["PROJECT", "MID", "FINAL", "SCORE", "HURUF"]

    # Isi Data
    table = []
    for i in range(len(NAMA)):
        row = [NIM[i], NAMA[i]]

        for nilai in ASSIGNMENTS[i]:
            row.append(str(nilai))
        row.append(f"{FINAL_ASSIGNMENT[i]}")

        for nilai in QUIZZES[i]:
            row.append(str(nilai))
        row.append(f"{FINAL_QUIZ[i]}")

        row.append(f"{PROJECT[i]}")
        row.append(f"{MID[i]}")
        row.append(f"{FINAL[i]}")
        row.append(f"{GRADE[i]}")
        row.append(GRADE_LETTER[i])

        table.append(row)
    return tabulate(table, headers=header, tablefmt="grid")

def frekuensi_grade():
    freq = {}
    for g in GRADE_LETTER:
        if g in freq:
            freq[g] += 1
        else:
            freq[g] = 1
    return freq

def sorting_logic(mode):
    IDX_GRADE = []
    for i in range(len(GRADE)): IDX_GRADE.append(i)
    for j in range(len(IDX_GRADE)):
        for k in range(j+1, len(GRADE)):
            if GRADE[IDX_GRADE[j]] > GRADE[IDX_GRADE[k]]:
                temp = IDX_GRADE[j]
                IDX_GRADE[j] = IDX_GRADE[k]
                IDX_GRADE[k] = temp
    
    result_str = ""
    if mode == 'a': # ascending
        result_str += '\n=== Urutan Nilai dari Terendah ke Tertinggi ===\n'
        for n in range(len(GRADE)):
            idx = IDX_GRADE[n]
            result_str += f'{GRADE[idx]} - {NAMA[idx]} ({GRADE_LETTER[idx]})\n'
    elif mode == 'b': # descending
        result_str += '\n=== Urutan Nilai dari Tertinggi ke Terendah ===\n'
        for n in range(len(GRADE)-1, -1, -1):
            idx = IDX_GRADE[n]
            result_str += f'{GRADE[idx]} - {NAMA[idx]} ({GRADE_LETTER[idx]})\n'        
    return result_str

def generate_full_report_string():
    full_text = "\tLAPORAN NILAI COMPUTER PROGRAMMING\n\n"
    
    full_text += "1. TABEL DATA NILAI\n"
    full_text += display_report() + "\n\n"
    
    idx_high, idx_low = highest_lowest()
    full_text += "2. HIGHEST AND LOWEST SCORE\n"
    full_text += f"   - Nilai Tertinggi : {GRADE[idx_high]} (Oleh: {NAMA[idx_high]})\n"
    full_text += f"   - Nilai Terendah  : {GRADE[idx_low]} (Oleh: {NAMA[idx_low]})\n\n"
    
    full_text += "3. PASS OR NOT PASS\n"
    txt_jum, txt_detail = tidak_lulus()
    if txt_jum is not None:
        full_text += f"   {txt_jum}"
        full_text += f"   Daftar siswa remedial:\n{txt_detail}\n"
    else:
        full_text += "   Selamat! Semua siswa lulus (Nilai >= 67).\n\n"

    full_text += "4. GRADE FREQUENCY\n"
    freq = frekuensi_grade()
    for g, count in sorted(freq.items()):
        full_text += f"   - Grade {g} : {count} orang\n"
    full_text += "\n"

    full_text += "5. RANKING KELAS (sorted dari Tertinggi ke Terendah)"
    full_text += sorting_logic('b')
    
    return full_text

# --- INTEGRASI STREAMLIT (INTERFACE) ---

# Set Up Session State
if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = []
if 'locked_jml_tugas' not in st.session_state:
    st.session_state.locked_jml_tugas = None
if 'locked_jml_quiz' not in st.session_state:
    st.session_state.locked_jml_quiz = None

# Fungsi Sinkronisasi data
def sync_data_to_globals():
    global NIM, NAMA, ASSIGNMENTS, FINAL_ASSIGNMENT, QUIZZES, FINAL_QUIZ
    global PROJECT, MID, FINAL, GRADE, GRADE_LETTER
    
    NIM.clear(); NAMA.clear(); ASSIGNMENTS.clear(); FINAL_ASSIGNMENT.clear()
    QUIZZES.clear(); FINAL_QUIZ.clear(); PROJECT.clear(); MID.clear()
    FINAL.clear(); GRADE.clear(); GRADE_LETTER.clear()
    
    for data in st.session_state.database_siswa:
        NIM.append(data['nim'])
        NAMA.append(data['nama'])
        ASSIGNMENTS.append(data['list_tugas'])
        QUIZZES.append(data['list_quiz'])
        
        nilai_akhir = hitung_nilai_akhir(
            data['proj'], data['mid'], data['final'], 
            data['list_tugas'], data['list_quiz']
        )
        nilai_akhir = int(nilai_akhir)
        GRADE.append(nilai_akhir)
        GRADE_LETTER.append(nilai_huruf(nilai_akhir))

sync_data_to_globals()

# === MAKING USER INTERFACE ===
st.title("🎓 Student Grading System")

menu = st.sidebar.selectbox("Pilih Menu", [
    "Input Data Baru", 
    "Tampilkan Semua Nilai", 
    "Frekuensi Grade", 
    "Sorting Nilai", 
    "Tampilkan Tabel Lengkap", 
    "Simpan ke File",
    "Reset Data"
])

if menu == "Input Data Baru":
    st.header("Input Data Mahasiswa")
    
    with st.form("form_input"):
        c1, c2 = st.columns(2)
        in_nama = c1.text_input("Nama Student")
        in_nim = c2.text_input("NIM")
        
        msg_tugas = "Masukkan nilai dipisahkan koma"
        msg_quiz = "Masukkan nilai dipisahkan koma"
        
        if st.session_state.locked_jml_tugas is not None:
            msg_tugas += f" (WAJIB {st.session_state.locked_jml_tugas} nilai)"
            msg_quiz += f" (WAJIB {st.session_state.locked_jml_quiz} nilai)"
            
        st.info(msg_tugas)
        in_tugas_str = st.text_input("Nilai Assignment", "")
        st.info(msg_quiz)
        in_quiz_str = st.text_input("Nilai Quiz", "")
        
        c3, c4, c5 = st.columns(3)
        in_proj = c3.number_input("Nilai Project (15%)", step=1, value=None)
        in_mid = c4.number_input("Nilai MID (25%)", step=1, value=None)
        in_fin = c5.number_input("Nilai FINAL (25%)", step=1, value=None)
        
        submit = st.form_submit_button("Simpan Data")
        
        if submit:
            if not in_nama or not in_nim:
                st.error("⚠️ Input Failed: Nama Mahasiswa atau NIM wajib diisi!")
            elif not in_tugas_str or not in_quiz_str:
                st.error("⚠️ Input Failed: Nilai Assignment atau Quiz belum diisi!")
            elif in_proj is None or in_mid is None or in_fin is None:
                st.error("⚠️ Input Failed: Nilai Project/Mid/Final belum diisi!")
            else:
                proj_validity = mid_validity = fin_validity = False
                if 0 <= in_proj <= 100: proj_validity = True
                if 0 <= in_mid <= 100: mid_validity = True
                if 0 <= in_fin <= 100: fin_validity = True
                
                if not (proj_validity and mid_validity and fin_validity):
                    st.error("⚠️ Input Error: Nilai Project, MID, dan Final harus berupa ANGKA BULAT antara 0-100.")
                    st.stop()
                else:
                    try:
                        list_tugas = []
                        for x in in_tugas_str.split(','):
                            val = int(x.strip()) 
                            if val < 0 or val > 100: raise ValueError("Range Error")
                            list_tugas.append(val)

                        list_quiz = []
                        for x in in_quiz_str.split(','):
                            val = int(x.strip())
                            if val < 0 or val > 100: raise ValueError("Range Error")
                            list_quiz.append(val)
                        
                        if st.session_state.locked_jml_tugas is not None:
                            if len(list_tugas) != st.session_state.locked_jml_tugas:
                                st.error(f"⛔ Input data failed! Wajib {st.session_state.locked_jml_tugas} nilai assignment.")
                                st.stop()
                            
                            if len(list_quiz) != st.session_state.locked_jml_quiz:
                                st.error(f"⛔ Input data failed! Wajib {st.session_state.locked_jml_quiz} nilai quiz.")
                                st.stop()
                        else:
                            st.session_state.locked_jml_tugas = len(list_tugas)
                            st.session_state.locked_jml_quiz = len(list_quiz)
                        
                        st.session_state.database_siswa.append({
                            'nama': in_nama, 'nim': in_nim,
                            'list_tugas': list_tugas, 'list_quiz': list_quiz,
                            'proj': in_proj, 'mid': in_mid, 'final': in_fin
                        })
                        st.success("Data berhasil disimpan!")
                        time.sleep(1)
                        st.rerun()
                    except ValueError:
                        st.error("Pastikan nilai Tugas/Quiz berupa angka bulat (0-100) dipisah koma!")

elif menu == "Tampilkan Semua Nilai":
    st.header("Daftar Nilai Akhir")
    if len(NAMA) > 0:
        st.text(tampilkan_nilai_final())
        high, low = highest_lowest()
        st.info(f'Nilai Tertinggi: {GRADE[high]} ({NAMA[high]})')
        st.info(f'Nilai Terendah: {GRADE[low]} ({NAMA[low]})')
    else:
        st.warning("Belum ada data.")

elif menu == "Frekuensi Grade":
    st.header("Frekuensi Grade")
    if len(GRADE_LETTER) > 0:
        freq = frekuensi_grade()
        for grade, jumlah in sorted(freq.items()):
            st.text(f"Grade {grade} : {jumlah} orang")
        st.bar_chart(freq, horizontal=True)
    else:
        st.warning("Belum ada data.")

elif menu == "Sorting Nilai":
    st.header("Sorting Nilai")
    if len(GRADE) > 0:
        sort_type = st.radio("Jenis Sorting:", ["Ascending (Kecil ke Besar)", "Descending (Besar ke Kecil)"])
        mode = 'a' if "Ascending" in sort_type else 'b'
        st.text(sorting_logic(mode))
    else:
        st.warning("Belum ada data.")

elif menu == "Tampilkan Tabel Lengkap":
    st.header("Laporan Lengkap")
    if len(NAMA) > 0:
        st.code(display_report())
        
        st.divider()
        st.subheader('Statistik')
        idx_max, idx_min = highest_lowest()
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**Tertinggi: {NAMA[idx_max]}**\n\n"
                       f"Score Akhir: {GRADE[idx_max]} ({GRADE_LETTER[idx_max]})\n\n"
                       f"**Rincian Bobot Nilai:**\n"
                       f"- Assignment (20%): {FINAL_ASSIGNMENT[idx_max]}\n"
                       f"- Quiz (15%): {FINAL_QUIZ[idx_max]}\n"
                       f"- Project (15%): {PROJECT[idx_max]}\n"
                       f"- Mid (25%): {MID[idx_max]}\n"
                       f"- Final (25%): {FINAL[idx_max]}")
        with col2:
            st.error(f"**Terendah: {NAMA[idx_min]}**\n\n"
                     f"Score Akhir: {GRADE[idx_min]} ({GRADE_LETTER[idx_min]})\n\n"
                     f"**Rincian Bobot Nilai:**\n"
                     f"- Assignment (20%): {FINAL_ASSIGNMENT[idx_min]}\n"
                     f"- Quiz (15%): {FINAL_QUIZ[idx_min]}\n"
                     f"- Project (15%): {PROJECT[idx_min]}\n"
                     f"- Mid (25%): {MID[idx_min]}\n"
                     f"- Final (25%): {FINAL[idx_min]}")
            
        jumlah_gagal_text, data_gagal = tidak_lulus()
        st.divider()
        st.subheader("Analisis Kelulusan")
        
        if jumlah_gagal_text is not None:
            st.warning(jumlah_gagal_text)
            with st.expander("Lihat daftar siswa remedial"):
                st.text(data_gagal)
        else:
            st.balloons()
            st.success("✅ Selamat! Semua siswa lulus.")
    else:
        st.warning("Belum ada data.")

elif menu == "Simpan ke File":
    st.header("Download Laporan Lengkap")
    if len(NAMA) > 0:
        laporan_lengkap = generate_full_report_string()
        st.download_button(
            label="💾 Download Student.txt",
            data=laporan_lengkap,
            file_name="Student.txt",
            mime="text/plain"
        )
    else:
        st.warning("Belum ada data untuk disimpan.")
        
elif menu == "Reset Data":
    st.header("Reset Data")
    st.warning("⚠️WARNING: Menghapus semua data!")
    if st.button("HAPUS SEMUA DATA", type="primary"):
        st.session_state.database_siswa = [] 
        st.session_state.locked_jml_tugas = None
        st.session_state.locked_jml_quiz = None
        st.success("Semua data berhasil dihapus.")
        time.sleep(1)
        st.rerun()