import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import json
import os
from datetime import datetime

class TebakAngkaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tebak Angka - TIOCV2C37")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Warna tema
        self.bg_color = '#2c3e50'
        self.frame_color = '#34495e'
        self.text_color = '#ecf0f1'
        self.accent_color = '#3498db'
        self.warning_color = '#e74c3c'
        self.success_color = '#2ecc71'
        self.title_color = '#f1c40f'
        
        # Inisialisasi leaderboard
        self.leaderboard_file = 'leaderboard.json'
        self.leaderboard_data = []
        self.load_leaderboard()
        
        # Variabel game
        self.kode_rahasia = 0
        self.riwayat_tebakan = []
        self.nyawa = 0
        self.start_time = 0
        self.player_name = ""
        self.tingkat_kesulitan = {
            'PEMULA': {'jarak': (1, 50), 'nyawa': 10, 'petunjuk': True, 'multiplier': 1},
            'STANDAR': {'jarak': (1, 100), 'nyawa': 7, 'petunjuk': True, 'multiplier': 2},
            'SULIT': {'jarak': (1, 200), 'nyawa': 5, 'petunjuk': False, 'multiplier': 3},
            'EKSTRIM': {'jarak': (1, 500), 'nyawa': 3, 'petunjuk': False, 'multiplier': 5}
        }
        self.level_terpilih = 'STANDAR'
        
        self.setup_ui()
        self.tampilkan_menu_utama()
    
    def setup_ui(self):
        self.style = ttk.Style()
        self.root.configure(bg=self.bg_color)
        
        # Frame style
        self.style.configure('TFrame', background=self.frame_color)
        self.style.configure('TLabel', background=self.frame_color, foreground=self.text_color, font=('Helvetica', 10))
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground=self.title_color)
        self.style.configure('Leaderboard.TLabel', font=('Helvetica', 10, 'bold'), foreground=self.title_color)
        
        # Button style
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.map('TButton',
            background=[('active', '#2980b9')],
            foreground=[('active', 'white')]
        )
        
        # Treeview style
        self.style.configure('Treeview', 
            background='#ecf0f1', 
            foreground='black', 
            rowheight=25, 
            fieldbackground='#ecf0f1',
            font=('Helvetica', 10)
        )
        self.style.configure('Treeview.Heading', 
            background='#3498db', 
            foreground='black', 
            font=('Helvetica', 10, 'bold')
        )
        self.style.map('Treeview', 
            background=[('selected', '#2980b9')],
            foreground=[('selected', 'white')]
        )
        
        # Main layout
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Header
        ttk.Label(self.header_frame, text="TIOCV2C37 - TEBAK ANGKA", style='Title.TLabel').pack()
        
        # Footer
        self.footer_text = tk.StringVar()
        self.update_footer_time()
        ttk.Label(
            self.footer_frame, 
            textvariable=self.footer_text,
            background=self.bg_color,
            foreground='#bdc3c7',
            font=('Helvetica', 8)
        ).pack(side=tk.RIGHT)
    
    def load_leaderboard(self):
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r') as f:
                    self.leaderboard_data = json.load(f)
            except:
                self.leaderboard_data = []
        else:
            self.leaderboard_data = []
    
    def save_leaderboard(self):
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.leaderboard_data, f)
    
    def add_to_leaderboard(self, name, level, score, time_taken, guesses):
        entry = {
            'name': name,
            'level': level,
            'score': score,
            'time': time_taken,
            'guesses': guesses,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.leaderboard_data.append(entry)
        # Sort by score descending
        self.leaderboard_data.sort(key=lambda x: x['score'], reverse=True)
        # Keep only top 10 entries
        if len(self.leaderboard_data) > 10:
            self.leaderboard_data = self.leaderboard_data[:10]
        self.save_leaderboard()
    
    def update_footer_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.footer_text.set(f"© 2023 Protokol Keamanan C37 | {current_time}")
        self.root.after(1000, self.update_footer_time)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def tampilkan_menu_utama(self):
        self.clear_content()
        
        # Menu utama frame
        menu_frame = ttk.Frame(self.content_frame)
        menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        ttk.Label(menu_frame, text="Pilih operasi:").pack(pady=(20, 10))
        
        btn_frame = ttk.Frame(menu_frame)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("MULAI GAME", self.minta_nama_pemain),
            ("LEADERBOARD", self.tampilkan_leaderboard),
            ("PANDUAN", self.tampilkan_panduan),
            ("KELUAR", self.root.quit)
        ]
        
        for text, cmd in buttons:
            ttk.Button(
                btn_frame, 
                text=text,
                command=cmd
            ).pack(fill=tk.X, pady=5)
        
        # Leaderboard preview frame
        leaderboard_frame = ttk.Frame(self.content_frame)
        leaderboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        ttk.Label(leaderboard_frame, text="TOP 5 LEADERBOARD", style='Leaderboard.TLabel').pack(pady=(20, 10))
        
        columns = ('Peringkat', 'Nama', 'Skor', 'Level')
        self.leaderboard_preview = ttk.Treeview(
            leaderboard_frame,
            columns=columns,
            show='headings',
            height=5
        )
        
        for col in columns:
            self.leaderboard_preview.heading(col, text=col)
            self.leaderboard_preview.column(col, width=80, anchor=tk.CENTER)
        
        # Configure tags for preview
        self.leaderboard_preview.tag_configure('gold', background='#FFD700')
        self.leaderboard_preview.tag_configure('silver', background='#C0C0C0')
        self.leaderboard_preview.tag_configure('bronze', background='#CD7F32')
        
        # Add sample data to preview
        self.update_leaderboard_preview()
        
        self.leaderboard_preview.pack(fill=tk.BOTH, expand=True)
    
    def update_leaderboard_preview(self):
        for item in self.leaderboard_preview.get_children():
            self.leaderboard_preview.delete(item)
        
        for i, entry in enumerate(self.leaderboard_data[:5], 1):
            if i == 1:
                tag = 'gold'
            elif i == 2:
                tag = 'silver'
            elif i == 3:
                tag = 'bronze'
            else:
                tag = ''
                
            self.leaderboard_preview.insert('', tk.END, values=(
                i,
                entry['name'],
                entry['score'],
                entry['level']
            ), tags=(tag))
    
    def minta_nama_pemain(self):
        self.clear_content()
        
        ttk.Label(self.content_frame, text="Masukkan nama Anda:").pack(pady=(50, 10))
        
        self.name_entry = ttk.Entry(self.content_frame, width=30)
        self.name_entry.pack(pady=10)
        self.name_entry.bind('<Return>', lambda e: self.set_nama_pemain())
        
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(
            btn_frame,
            text="LANJUT",
            command=self.set_nama_pemain
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="KEMBALI",
            command=self.tampilkan_menu_utama
        ).pack(side=tk.LEFT, padx=5)
    
    def set_nama_pemain(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Peringatan", "Nama tidak boleh kosong!")
            return
        self.tampilkan_level()
    
    def tampilkan_leaderboard(self):
        self.clear_content()
        
        ttk.Label(self.content_frame, text="LEADERBOARD", style='Title.TLabel').pack(pady=(10, 20))
        
        columns = ('Peringkat', 'Nama', 'Skor', 'Level', 'Waktu', 'Tebakan', 'Tanggal')
        self.leaderboard_tree = ttk.Treeview(
            self.content_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        # Configure tags for different rows
        self.leaderboard_tree.tag_configure('gold', background='#FFD700', foreground='black')
        self.leaderboard_tree.tag_configure('silver', background='#C0C0C0', foreground='black')
        self.leaderboard_tree.tag_configure('bronze', background='#CD7F32', foreground='black')
        self.leaderboard_tree.tag_configure('top10', background='#f8f9fa', foreground='black')
        
        for col in columns:
            self.leaderboard_tree.heading(col, text=col)
            self.leaderboard_tree.column(col, width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(self.leaderboard_tree, orient="vertical", command=self.leaderboard_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.leaderboard_tree.configure(yscrollcommand=scrollbar.set)
        
        # Add data to leaderboard with different colors for top 3 positions
        for i, entry in enumerate(self.leaderboard_data, 1):
            if i == 1:
                tag = 'gold'
            elif i == 2:
                tag = 'silver'
            elif i == 3:
                tag = 'bronze'
            else:
                tag = 'top10'
                
            self.leaderboard_tree.insert('', tk.END, values=(
                i,
                entry['name'],
                entry['score'],
                entry['level'],
                f"{entry['time']:.1f} detik",
                entry['guesses'],
                entry['date']
            ), tags=(tag))
        
        self.leaderboard_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        ttk.Button(
            self.content_frame,
            text="KEMBALI KE MENU UTAMA",
            command=self.tampilkan_menu_utama
        ).pack(fill=tk.X, pady=(10, 0))
    
    def tampilkan_level(self):
        self.clear_content()
        
        ttk.Label(self.content_frame, text="Pilih Tingkat Kesulitan:").pack(pady=(20, 10))
        
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        for level in self.tingkat_kesulitan:
            text = f"{level} (1-{self.tingkat_kesulitan[level]['jarak'][1]}, {self.tingkat_kesulitan[level]['nyawa']} nyawa)"
            ttk.Button(
                btn_frame,
                text=text,
                command=lambda l=level: self.set_level(l)
            ).pack(fill=tk.X, pady=3)
        
        ttk.Button(
            self.content_frame,
            text="KEMBALI KE MENU UTAMA",
            command=self.tampilkan_menu_utama
        ).pack(fill=tk.X, pady=(20, 0))
    
    def set_level(self, level):
        self.level_terpilih = level
        self.mulai_game()
    
    def mulai_game(self):
        self.clear_content()
        self.riwayat_tebakan = []
        level = self.tingkat_kesulitan[self.level_terpilih]
        self.nyawa = level['nyawa']
        self.kode_rahasia = random.randint(*level['jarak'])
        self.start_time = time.time()

        # Header game
        ttk.Label(
            self.content_frame,
            text=f"LEVEL: {self.level_terpilih} | ANGKA RAHASIA ANTARA 1-{level['jarak'][1]}",
            font=('Helvetica', 10, 'bold')
        ).pack(pady=(0, 10))

        # Player info
        ttk.Label(
            self.content_frame,
            text=f"Pemain: {self.player_name}",
            font=('Helvetica', 10)
        ).pack(pady=(0, 5))

        # Nyawa tersisa
        self.nyawa_label = ttk.Label(
            self.content_frame,
            text=f"NYAWA TERSISA: {self.nyawa}",
            font=('Helvetica', 10, 'bold'),
            foreground=self.accent_color
        )
        self.nyawa_label.pack(pady=(0, 20))

        # Input tebakan
        input_frame = ttk.Frame(self.content_frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Masukkan tebakan Anda:").pack(side=tk.LEFT, padx=5)
        
        self.tebakan_entry = ttk.Entry(input_frame, width=10)
        self.tebakan_entry.pack(side=tk.LEFT, padx=5)
        self.tebakan_entry.bind('<Return>', lambda e: self.cek_tebakan())
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="TEBAK",
            command=self.cek_tebakan
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            btn_frame,
            text="BATAL",
            command=self.batalkan_tebakan
        ).pack(side=tk.LEFT, padx=2)

        # Petunjuk frame
        self.petunjuk_frame = ttk.LabelFrame(self.content_frame, text="Petunjuk")
        self.petunjuk_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.petunjuk_text = tk.Text(
            self.petunjuk_frame,
            height=6,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.petunjuk_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Riwayat tebakan
        ttk.Label(self.content_frame, text="RIWAYAT TEBAKAN:").pack(pady=(5, 0))

        columns = ('No', 'Tebakan', 'Petunjuk')
        self.riwayat_tree = ttk.Treeview(
            self.content_frame,
            columns=columns,
            show='headings',
            height=8
        )

        for col in columns:
            self.riwayat_tree.heading(col, text=col)
            self.riwayat_tree.column(col, width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(self.riwayat_tree, orient="vertical", command=self.riwayat_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.riwayat_tree.configure(yscrollcommand=scrollbar.set)

        self.riwayat_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Tombol aksi
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            action_frame,
            text="BERI PETUNJUK",
            command=self.beri_petunjuk
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame,
            text="ULANGI GAME",
            command=self.mulai_game
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame,
            text="KEMBALI KE MENU",
            command=self.tampilkan_menu_utama
        ).pack(side=tk.RIGHT, padx=5)

        self.update_petunjuk(None, level)
    
    def hitung_skor(self, waktu, tebakan, level):
        base_score = 1000
        time_factor = max(1, 30 - waktu)  # Bonus for faster completion
        guess_factor = max(1, 10 - tebakan)  # Bonus for fewer guesses
        level_multiplier = self.tingkat_kesulitan[level]['multiplier']
        
        score = base_score * level_multiplier + (time_factor * 10) + (guess_factor * 20)
        return int(score)
    
    def cek_tebakan(self):
        try:
            tebakan = int(self.tebakan_entry.get())
            min_val, max_val = self.tingkat_kesulitan[self.level_terpilih]['jarak']
            
            if tebakan < min_val or tebakan > max_val:
                messagebox.showwarning(
                    "Peringatan",
                    f"Masukkan angka antara {min_val} dan {max_val}!"
                )
                return
                
            self.riwayat_tebakan.append(tebakan)
            self.nyawa -= 1
            self.nyawa_label.config(text=f"NYAWA TERSISA: {self.nyawa}")
            
            # Update petunjuk dan riwayat
            level = self.tingkat_kesulitan[self.level_terpilih]
            self.update_petunjuk(tebakan, level)
            self.update_riwayat_tree()
            
            if tebakan == self.kode_rahasia:
                waktu_selesai = time.time() - self.start_time
                skor = self.hitung_skor(waktu_selesai, len(self.riwayat_tebakan), self.level_terpilih)
                
                self.add_to_leaderboard(
                    self.player_name,
                    self.level_terpilih,
                    skor,
                    waktu_selesai,
                    len(self.riwayat_tebakan)
                )
                
                messagebox.showinfo(
                    "Selamat!",
                    f"Tebakan Anda BENAR!\n"
                    f"Angka rahasianya adalah {self.kode_rahasia}.\n"
                    f"Waktu: {waktu_selesai:.1f} detik\n"
                    f"Tebakan: {len(self.riwayat_tebakan)}\n"
                    f"Skor: {skor}"
                )
                self.tampilkan_menu_utama()
                return
            elif self.nyawa <= 0:
                messagebox.showerror(
                    "Game Over",
                    f"Nyawa habis! Angka rahasianya adalah {self.kode_rahasia}."
                )
                self.tampilkan_menu_utama()
                return
            
            self.tebakan_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
            self.tebakan_entry.delete(0, tk.END)
    
    def update_riwayat_tree(self):
        # Clear existing items
        for item in self.riwayat_tree.get_children():
            self.riwayat_tree.delete(item)
            
        # Add new items
        for i, tebakan in enumerate(self.riwayat_tebakan, 1):
            if tebakan == self.kode_rahasia:
                petunjuk = "TEPAT"
            elif tebakan < self.kode_rahasia:
                petunjuk = "TERLALU RENDAH"
            else:
                petunjuk = "TERLALU TINGGI"
                
            self.riwayat_tree.insert(
                '', 
                tk.END, 
                values=(i, tebakan, petunjuk)
            )
    
    def update_petunjuk(self, tebakan, level):
        self.petunjuk_text.config(state=tk.NORMAL)
        self.petunjuk_text.delete(1.0, tk.END)
        
        if tebakan is None or not self.riwayat_tebakan:
            self.petunjuk_text.insert(tk.END, 
                "Masukkan tebakan pertama Anda\n"
                f"Jangkauan angka: 1-{level['jarak'][1]}\n"
                f"Nyawa tersisa: {self.nyawa}")
            self.petunjuk_text.config(state=tk.DISABLED)
            return
        
        tebakan_terakhir = self.riwayat_tebakan[-1]
        selisih = abs(tebakan_terakhir - self.kode_rahasia)
        
        petunjuk = f"=== Tebakan Terakhir: {tebakan_terakhir} ===\n\n"
        
        if tebakan_terakhir < self.kode_rahasia:
            petunjuk += "➤ Tebakan Anda TERLALU RENDAH\n"
        else:
            petunjuk += "➤ Tebakan Anda TERLALU TINGGI\n"
        
        if selisih <= 5:
            petunjuk += "★ Hampir benar! Hanya selisih ±5 angka\n"
            petunjuk += f"Coba antara {self.kode_rahasia-5} dan {self.kode_rahasia+5}\n"
        elif selisih <= 15:
            petunjuk += "○ Mendekati! Selisih sekitar 6-15 angka\n"
            petunjuk += f"Coba antara {self.kode_rahasia-15} dan {self.kode_rahasia+15}\n"
        elif selisih <= 30:
            petunjuk += "△ Cukup jauh. Selisih sekitar 16-30 angka\n"
        else:
            petunjuk += "✖ Masih sangat jauh dari target\n"
        
        if level['petunjuk']:
            petunjuk += "\n[PETUNJUK LANJUTAN]\n"
            if self.kode_rahasia % 2 == 0:
                petunjuk += "● Kode rahasia adalah angka genap\n"
            else:
                petunjuk += "● Kode rahasia adalah angka ganjil\n"
                
            if self.kode_rahasia < level['jarak'][1]//2:
                petunjuk += "● Kode berada di paruh BAWAH range\n"
            else:
                petunjuk += "● Kode berada di paruh ATAS range\n"
        
        petunjuk += f"\nNyawa tersisa: {self.nyawa}"
        
        self.petunjuk_text.insert(tk.END, petunjuk)
        self.petunjuk_text.config(state=tk.DISABLED)
    
    def beri_petunjuk(self):
        if not self.tingkat_kesulitan[self.level_terpilih]['petunjuk']:
            messagebox.showinfo(
                "Info",
                "Mode ini tidak menyediakan petunjuk!"
            )
            return
            
        if not self.riwayat_tebakan:
            messagebox.showinfo(
                "Info",
                "Anda belum melakukan tebakan apapun!"
            )
            return
            
        last_guess = self.riwayat_tebakan[-1]
        if last_guess == self.kode_rahasia:
            messagebox.showinfo(
                "Info",
                "Tebakan terakhir Anda sudah benar!"
            )
        elif last_guess < self.kode_rahasia:
            selisih = self.kode_rahasia - last_guess
            if selisih <= 5:
                petunjuk = "Hampir! Sedikit lebih tinggi"
            else:
                petunjuk = "Masih jauh lebih tinggi"
            messagebox.showinfo("Petunjuk", petunjuk)
        else:
            selisih = last_guess - self.kode_rahasia
            if selisih <= 5:
                petunjuk = "Hampir! Sedikit lebih rendah"
            else:
                petunjuk = "Masih jauh lebih rendah"
            messagebox.showinfo("Petunjuk", petunjuk)
    
    def batalkan_tebakan(self):
        if self.riwayat_tebakan:
            tebakan_dibatalkan = self.riwayat_tebakan.pop()
            self.nyawa += 1
            self.nyawa_label.config(text=f"NYAWA TERSISA: {self.nyawa}")
            
            level = self.tingkat_kesulitan[self.level_terpilih]
            if self.riwayat_tebakan:
                self.update_petunjuk(self.riwayat_tebakan[-1], level)
            else:
                self.update_petunjuk(None, level)
            
            self.update_riwayat_tree()
            messagebox.showinfo("Info", f"Tebakan {tebakan_dibatalkan} dibatalkan")
        else:
            messagebox.showwarning("Peringatan", "Tidak ada tebakan untuk dibatalkan")
    
    def tampilkan_panduan(self):
        self.clear_content()
        
        panduan_text = """
        PANDUAN TEBAK ANGKA
        
        1. Pilih tingkat kesulitan yang diinginkan:
           - Pemula: Angka 1-50 dengan 10 nyawa
           - Standar: Angka 1-100 dengan 7 nyawa
           - Sulit: Angka 1-200 dengan 5 nyawa
           - Ekstrim: Angka 1-500 dengan 3 nyawa
        
        2. Masukkan tebakan angka Anda pada kolom yang disediakan
        
        3. Setiap tebakan yang salah akan mengurangi nyawa Anda
        
        4. Jika nyawa habis sebelum angka berhasil ditebak, Anda kalah
        
        5. Beberapa level menyediakan petunjuk untuk membantu menebak
        
        6. Riwayat tebakan akan ditampilkan untuk membantu analisis
        
        7. Anda dapat membatalkan tebakan terakhir untuk mengembalikan nyawa
        
        8. Skor dihitung berdasarkan:
           - Tingkat kesulitan
           - Waktu penyelesaian
           - Jumlah tebakan
           - Nyawa tersisa
        
        Selamat bermain!
        """
        
        text_widget = tk.Text(
            self.content_frame, 
            wrap=tk.WORD, 
            font=('Helvetica', 10), 
            padx=10, 
            pady=10,
            height=15
        )
        text_widget.insert(tk.END, panduan_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(
            self.content_frame,
            text="KEMBALI KE MENU UTAMA",
            command=self.tampilkan_menu_utama
        ).pack(fill=tk.X, pady=(10, 0))

if __name__ == "__main__":
    root = tk.Tk()
    app = TebakAngkaGUI(root)
    root.mainloop()