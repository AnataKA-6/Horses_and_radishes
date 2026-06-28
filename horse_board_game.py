import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import random
import json
import math
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
import os

import sys

def resource_path(relative_path):
    """Получить путь к ресурсам (работает и в EXE, и в .py)"""
    try:
        # PyInstaller создаёт временную папку _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Попытка импорта pygame-ce
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except ImportError:
    try:
        import pygame_ce as pygame
        pygame.mixer.init()
        SOUND_AVAILABLE = True
    except ImportError:
        SOUND_AVAILABLE = False
        print("Pygame не установлен. Звук будет отключён. Установите: pip install pygame-ce")

# Игровые константы
QUARTERS_PER_GOLD = 4
MAX_LAND = 10
PRICE_STABLE = 1 * QUARTERS_PER_GOLD
PRICE_FIELD = 1 * QUARTERS_PER_GOLD
PRICE_RADISH = 1
PRICE_WATER = 1
PRICE_UPGRADE = 1
PRICE_RACE_ENTRY = 1 * QUARTERS_PER_GOLD
TRAINING_CIRCLE_MAX = 10
TRAINING_UPGRADES_MAX = 4
RADISH_PER_FIELD = 4
GAME_VERSION = "4.0"

# ========== ИМЕНА ЛОШАДЕЙ ==========
HORSE_NAMES_MALE = [
    "Гром", "Молния", "Ветер", "Сокол", "Буран", "Титан",
    "Алмаз", "Рубин", "Янтарь", "Шторм", "Тайфун", "Ураган",
    "Феникс", "Пегас", "Ахилл", "Гектор", "Одиссей", "Атлант",
    "Вихрь", "Богатырь", "Добрыня", "Илья", "Святогор", "Булат",
    "Барс", "Леопард", "Тигр", "Орёл", "Ястреб", "Кречет",
    "Верный", "Смелый", "Быстрый", "Сильный", "Гордый", "Вольный",
    "Золотой", "Серебряный", "Бронзовый", "Жемчуг", "Агат",
    "Север", "Байкал", "Эльбрус", "Казбек", "Урал", "Алтай"
]

HORSE_NAMES_FEMALE = [
    "Заря", "Искра", "Гроза", "Метель", "Радуга", "Солнце", "Луна", "Звезда",
    "Сапфир", "Бриз", "Руби", "Малахит", "Донна", "Алтайка", "Саянка"
]

HORSE_NAMES = HORSE_NAMES_MALE + HORSE_NAMES_FEMALE

# ========== ИМЕНА ВЛАДЕЛЬЦЕВ ЛОШАДЕЙ (ФЕРМЕРОВ) ==========
OWNER_NAMES = [
    "Граф Орлов",
    "Князь Бобринский",
    "Господин Вронский",
    "Барон фон Штраус",
    "Граф Шереметев",
    "Князь Голицын",
    "Барон Корф",
    "Граф Разумовский"
]

OWNER_COLORS = {
    "Граф Орлов": "#FFD700",
    "Князь Бобринский": "#C0C0C0",
    "Господин Вронский": "#CD7F32",
    "Барон фон Штраус": "#8B4513",
    "Граф Шереметев": "#FF6B6B",
    "Князь Голицын": "#4ECDC4",
    "Барон Корф": "#45B7D1",
    "Граф Разумовский": "#96CEB4"
}

OWNER_WEALTH = {
    "Граф Орлов": 4,
    "Князь Бобринский": 3,
    "Господин Вронский": 2,
    "Барон фон Штраус": 1,
    "Граф Шереметев": 3,
    "Князь Голицын": 2,
    "Барон Корф": 1,
    "Граф Разумовский": 4
}

# ========== ИМЕНА БОТОВ (ИГРОКОВ-ИИ) ==========
BOT_NAMES = [
    "AI_Стальной", "AI_Быстрый", "AI_Богатый", "AI_Хитрый",
    "AI_Смелый", "AI_Мудрый", "AI_Ловкий", "AI_Сильный",
    "AI_Вольный", "AI_Гордый", "AI_Верный", "AI_Буйный",
    "AI_Тихий", "AI_Яркий", "AI_Светлый", "AI_Тёмный",
    "AI_Добрый", "AI_Злой", "AI_Весёлый", "AI_Серьёзный"
]

# ========== ЦВЕТА ИГРОКОВ ==========
PLAYER_COLORS = ["#2E5E2E", "#2E4E6E", "#6E3E2E", "#4E2E6E"]

# ========== ДНИ НЕДЕЛИ ==========
WEEKDAYS = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
WEEKDAY_EVENTS = {
    "ПН": "🌱 Посадка редисок",
    "ВТ": "🏇 Тренировки",
    "СР": "🏇 Тренировки",
    "ЧТ": "🏇 Тренировки",
    "ПТ": "🏇 Тренировки",
    "СБ": "🏇 Тренировки",
    "ВС": "🏆 Скачки + Аукцион + Сбор урожая + Прокачки"
}

UPGRADE_COLORS = {
    'speed': '#FF4444',
    'radish': '#00d632',
    'water': '#4444FF',
    'empty': '#333333',
    'pending': '#FFFFFF'
}

UPGRADE_EMOJI = {
    'speed': '⚫',   # будет красным
    'radish': '⚫',  # будет зелёным
    'water': '⚫',   # будет синим
    'empty': '⚫',   # будет серым
    'pending': '⚫'  # будет белым или жёлтым
}

# ========== ХАРАКТЕРИСТИКИ ЛОШАДЕЙ ПО УРОВНЯМ ==========
HORSE_LEVELS = {
    1: {
        'base_food': 1,
        'base_water': 1,
        'base_speed': -1,
        'cost': 5 * QUARTERS_PER_GOLD,
        'icon': '🐴',
        'rewards': {
            'care': 2 * QUARTERS_PER_GOLD,      # 2 зол. за содержание
            'train': 2 * QUARTERS_PER_GOLD,     # 2 зол. за прокачку
            'win_race': 5 * QUARTERS_PER_GOLD,  # 5 зол. за победу
        }
    },
    2: {
        'base_food': 2,
        'base_water': 1,
        'base_speed': 0,
        'cost': 10 * QUARTERS_PER_GOLD,
        'icon': '🏇',
        'rewards': {
            'care': 2 * QUARTERS_PER_GOLD,      # 2 зол. за содержание
            'train': 1 * QUARTERS_PER_GOLD,     # 1 зол. за прокачку
            'win_race': 3 * QUARTERS_PER_GOLD,  # 3 зол. за победу
        }
    },
    3: {
        'base_food': 2,
        'base_water': 2,
        'base_speed': 1,
        'cost': 20 * QUARTERS_PER_GOLD,
        'icon': '🦄',
        'rewards': {
            'care': 2 * QUARTERS_PER_GOLD,      # 2 зол. за содержание
            'train': 2,                         # 2 четвертака за прокачку
            'win_race': 2 * QUARTERS_PER_GOLD,  # 2 зол. за победу
        }
    }
}

def get_version_string():
    """Возвращает строку с версией игры"""
    return f"Версия {GAME_VERSION}"

class SoundManager:
    def __init__(self):
        self.enabled = SOUND_AVAILABLE
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = True
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.current_music = None
        self.looped_sounds = []
        self.load_sounds()
    
    def load_sounds(self):
        sounds_dir = Path(resource_path("sounds"))
        sounds_dir.mkdir(exist_ok=True)
        
        sound_files = {
            'click': 'click.wav',
            'hover': 'hover.wav',
            'train': 'train.wav',
            'train_fail': 'train_fail.wav',
            'race_start': 'race_start.wav',
            'race_finish': 'race_finish.wav',
            'lucky': 'lucky.wav',
            'unlucky': 'unlucky.wav',
            'upgrade': 'upgrade.wav',
            'buy': 'buy.wav',
            'sell': 'sell.wav',
            'error': 'error.wav',
            'shoot': 'shoot.wav',
            'horses_run': 'horses_run.wav',
            'nomoney': 'nomoney.wav',
            'nugno_bolshe_redisok_i_vodii': 'nugno_bolshe_redisok_i_vodii.wav',
            'nugno_bolshe_vodii': 'nugno_bolshe_vodii.wav',
            'nugno_bolshe_redisok': 'nugno_bolshe_redisok.wav',
            'nash_geroi_mertv': 'nash_geroi_mertv.wav',
            'win': 'win.wav',
            'lose': 'lose.wav'
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = sounds_dir / filename
            if sound_path.exists() and self.enabled:
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(str(sound_path))
                    self.sounds[sound_name].set_volume(self.sfx_volume)
                except:
                    pass
            else:
                self.sounds[sound_name] = None
        
        music_path = Path(resource_path("sounds/background.mp3"))
        if music_path.exists() and self.enabled:
            self.current_music = str(music_path)
    
    def play_hover(self):
        """Воспроизводит звук наведения мыши (с низкой громкостью)"""
        if self.enabled and self.sfx_enabled and self.sounds.get('hover'):
            try:
                # Устанавливаем меньшую громкость для звука наведения
                self.sounds['hover'].set_volume(self.sfx_volume * 0.5)
                self.sounds['hover'].play()
                # Возвращаем обычную громкость для других звуков
                self.sounds['hover'].set_volume(self.sfx_volume)
            except:
                pass

    def play_music(self):
        if self.enabled and self.music_enabled and self.current_music:
            try:
                pygame.mixer.music.load(self.current_music)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)
            except:
                pass
    
    def stop_music(self):
        if self.enabled:
            pygame.mixer.music.stop()
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                try:
                    sound.set_volume(self.sfx_volume)
                except:
                    pass
        # Обновляем громкость зацикленных звуков
        for sound_name in self.looped_sounds:
            if self.sounds.get(sound_name):
                try:
                    self.sounds[sound_name].set_volume(self.sfx_volume)
                except:
                    pass
    
    def play(self, sound_name, loops=0):
        """
        Воспроизводит звук
        loops=0 - один раз
        loops=-1 - бесконечно (зацикленный)
        """
        if self.enabled and self.sfx_enabled and self.sounds.get(sound_name):
            try:
                self.sounds[sound_name].play(loops)
                # Запоминаем зацикленные звуки
                if loops == -1 and sound_name not in self.looped_sounds:
                    self.looped_sounds.append(sound_name)
            except:
                pass

    def pause_music(self):
        """Приостанавливает фоновую музыку"""
        if self.enabled and self.music_enabled:
            try:
                pygame.mixer.music.pause()
            except:
                pass
    
    def unpause_music(self):
        """Возобновляет фоновую музыку"""
        if self.enabled and self.music_enabled:
            try:
                pygame.mixer.music.unpause()
            except:
                pass
    
    def stop_sound(self, sound_name):
        """Останавливает определённый звук"""
        if self.enabled and self.sfx_enabled and self.sounds.get(sound_name):
            try:
                self.sounds[sound_name].stop()
            except:
                pass

    def stop_all_sounds(self):
        """Останавливает все звуковые эффекты (включая зацикленные)"""
        if self.enabled:
            for sound in self.sounds.values():
                if sound:
                    try:
                        sound.stop()
                    except:
                        pass
            self.looped_sounds = []  # Очищаем список зацикленных

    def toggle_sfx(self, enabled):
        """Включает/выключает звуковые эффекты"""
        self.sfx_enabled = enabled
        if not enabled:
            self.stop_all_sounds()  # Останавливаем все звуки при выключении
        else:
            self.play('click')  # Воспроизводим звук при включении

    def get_sound_length(self, sound_name):
        """Возвращает длительность звука в миллисекундах"""
        if self.enabled and self.sounds.get(sound_name):
            try:
                return int(self.sounds[sound_name].get_length() * 1000)
            except:
                pass
        return 2500  # значение по умолчанию

    def fade_out_music(self, duration_ms=2000, target_volume=0.0, step_ms=50):
        """Плавно уменьшает громкость музыки до target_volume за duration_ms миллисекунд"""
        if not self.enabled or not self.music_enabled:
            return
        
        try:
            current_volume = self.music_volume
            steps = duration_ms // step_ms
            if steps <= 0:
                return
            
            volume_step = (current_volume - target_volume) / steps
            
            def fade_step(current_step=0):
                if current_step < steps:
                    new_volume = current_volume - (volume_step * (current_step + 1))
                    new_volume = max(target_volume, min(self.music_volume, new_volume))
                    pygame.mixer.music.set_volume(new_volume)
                    self.root.after(step_ms, lambda: fade_step(current_step + 1))
                else:
                    if target_volume == 0:
                        pygame.mixer.music.pause()
            
            # Сохраняем исходную громкость для восстановления
            self.original_music_volume = current_volume
            fade_step()
        except:
            pass
    
    def fade_in_music(self, duration_ms=2000, target_volume=None, step_ms=50):
        """Плавно увеличивает громкость музыки до target_volume (или исходной) за duration_ms миллисекунд"""
        if not self.enabled or not self.music_enabled:
            return
        
        try:
            # Возобновляем музыку, если она была на паузе
            pygame.mixer.music.unpause()
            
            start_volume = 0.0
            if target_volume is None:
                target_volume = getattr(self, 'original_music_volume', 0.5)
            
            steps = duration_ms // step_ms
            if steps <= 0:
                return
            
            volume_step = target_volume / steps
            
            def fade_step(current_step=0):
                if current_step < steps:
                    new_volume = volume_step * (current_step + 1)
                    new_volume = min(target_volume, new_volume)
                    pygame.mixer.music.set_volume(new_volume)
                    self.root.after(step_ms, lambda: fade_step(current_step + 1))
                else:
                    pygame.mixer.music.set_volume(target_volume)
                    self.music_volume = target_volume
            
            fade_step()
        except:
            pass
    
    def set_root(self, root):
        """Устанавливает ссылку на root для использования after"""
        self.root = root

class ToastNotification:
    def __init__(self, parent, message, duration=5000, icon="✅"):
        self.parent = parent
        self.message = message
        self.duration = duration
        self.icon = icon
        self._destroyed = False
        self._fading = False
        
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.configure(bg='#2a3a2a', relief='ridge', bd=2)
        self.window.attributes('-alpha', 0.95)
        
        # Фрейм с тенью
        frame = tk.Frame(self.window, bg='#2a3a2a')
        frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Внутренний фрейм с содержимым
        inner_frame = tk.Frame(frame, bg='#2a3a2a', relief='raised', bd=1)
        inner_frame.pack(fill='both', expand=True, padx=8, pady=6)
        
        # Создаём метку с переносом текста
        label = tk.Label(inner_frame, text=f"{icon} {message}", font=('Arial', 10, 'bold'),
                        bg='#2a3a2a', fg='#FFD700', wraplength=310, justify='left')
        label.pack(padx=5, pady=5)
        
        # Вычисляем позицию
        self.window.update_idletasks()
        label_height = label.winfo_reqheight()
        total_height = label_height + 30
        
        x = parent.winfo_x() + parent.winfo_width() - 370
        y = parent.winfo_y() + parent.winfo_height() - total_height - 20
        
        self.window.geometry(f"350x{total_height}+{x}+{y}")
        
        # ✅ Запускаем таймер на плавное исчезновение через duration мс
        self.window.after(duration, self.start_fade_out)
    
    def start_fade_out(self):
        """Начинает плавное исчезновение"""
        if self._destroyed:
            return
        self._fading = True
        self.fade_out(0.95)
    
    def fade_out(self, alpha):
        """Плавно уменьшает прозрачность"""
        if self._destroyed:
            return
        
        if alpha > 0:
            alpha -= 0.05
            try:
                self.window.attributes('-alpha', alpha)
                self.window.after(30, lambda: self.fade_out(alpha))
            except (tk.TclError, AttributeError):
                self._destroyed = True
        else:
            # ✅ Когда alpha == 0 - уничтожаем окно
            self.close()
    
    def close(self):
        """Принудительно закрывает уведомление"""
        if self._destroyed:
            return
        self._destroyed = True
        try:
            self.window.destroy()
        except:
            pass

class ToastManager:
    """Менеджер для отображения уведомлений в столбец"""
    def __init__(self, parent):
        self.parent = parent
        self.toasts = []  # Список активных уведомлений
        self.max_toasts = 5  # Максимум видимых уведомлений
        self.spacing = 5  # Отступ между уведомлениями
        self.container = None
        
        # Создаем контейнер для уведомлений
        self.create_container()
        
        # Обновляем позицию при изменении размера окна
        parent.bind('<Configure>', lambda e: self.update_position())
    
    def create_container(self):
        """Создает контейнер для уведомлений"""
        # Если старый контейнер существует - уничтожаем его
        if self.container:
            try:
                self.container.destroy()
            except:
                pass
            self.container = None
        
        # Создаем новый контейнер
        self.container = tk.Toplevel(self.parent)
        self.container.overrideredirect(True)
        self.container.configure(bg='#1a2a1a')
        self.container.attributes('-alpha', 0.0)  # Прозрачный фон
        self.container.attributes('-topmost', True)  # Поверх всех окон
        self.container.geometry("370x200")  # Фиксированный размер
        
        # Позиционируем
        self.update_position()
    
    def ensure_container_exists(self):
        """Проверяет, существует ли контейнер, и создает его при необходимости"""
        try:
            if self.container is None:
                self.create_container()
                return
            # Проверяем, существует ли окно
            if not self.container.winfo_exists():
                self.create_container()
                return
        except (tk.TclError, AttributeError):
            self.create_container()
    
    def update_position(self):
        """Обновляет позицию контейнера"""
        try:
            if self.container is None:
                return
            if not self.container.winfo_exists():
                return
        except (tk.TclError, AttributeError):
            return
        
        # ✅ ИСПРАВЛЕНО: позиционируем в правом нижнем углу
        x = self.parent.winfo_x() + self.parent.winfo_width() - 390
        y = self.parent.winfo_y() + self.parent.winfo_height() - 220
        
        try:
            self.container.geometry(f"370x200+{x}+{y}")
        except:
            pass
    
    def show_toast(self, message, icon="✅", duration=5000):
        """Добавляет новое уведомление"""
        # ✅ Убеждаемся, что контейнер существует
        self.ensure_container_exists()
        
        # Создаем уведомление
        toast = ToastItem(self, message, icon, duration)
        self.toasts.append(toast)
        
        # Если уведомлений больше максимума - удаляем самое старое
        if len(self.toasts) > self.max_toasts:
            oldest = self.toasts.pop(0)
            oldest.close()
        
        # Обновляем позиции всех уведомлений
        self.update_toast_positions()
    
    def remove_toast(self, toast):
        """Удаляет уведомление из списка"""
        if toast in self.toasts:
            self.toasts.remove(toast)
        self.update_toast_positions()
    
    def update_toast_positions(self):
        """Обновляет позиции всех уведомлений (снизу вверх)"""
        # ✅ Убеждаемся, что контейнер существует
        self.ensure_container_exists()
        
        # Сортируем по времени добавления (старые снизу)
        for i, toast in enumerate(reversed(self.toasts)):
            # Каждое следующее уведомление выше на (высота + отступ)
            y_offset = i * (toast.get_height() + self.spacing)
            toast.move_to(y_offset)
    
    def clear_all(self):
        """Очищает все уведомления"""
        for toast in self.toasts[:]:
            toast.close()
        self.toasts.clear()


class ToastItem:
    """Отдельное уведомление в столбце"""
    def __init__(self, manager, message, icon="✅", duration=5000):
        self.manager = manager
        self.message = message
        self.icon = icon
        self.duration = duration
        self._destroyed = False
        self._fading = False
        self.height = 0
        self.window = None
        
        # ✅ Проверяем, что контейнер существует
        self.manager.ensure_container_exists()
        
        # Создаем окно уведомления
        try:
            self.window = tk.Toplevel(self.manager.container)
            self.window.overrideredirect(True)
            self.window.configure(bg='#2a3a2a', relief='ridge', bd=2)
            self.window.attributes('-alpha', 0.0)  # Начинаем с прозрачного
            self.window.attributes('-topmost', True)  # Поверх всех окон
        except (tk.TclError, AttributeError):
            # Если не удалось создать - пересоздаем контейнер и пробуем снова
            self.manager.create_container()
            self.window = tk.Toplevel(self.manager.container)
            self.window.overrideredirect(True)
            self.window.configure(bg='#2a3a2a', relief='ridge', bd=2)
            self.window.attributes('-alpha', 0.0)
            self.window.attributes('-topmost', True)
        
        # Контент
        frame = tk.Frame(self.window, bg='#2a3a2a')
        frame.pack(fill='both', expand=True, padx=10, pady=8)
        
        label = tk.Label(frame, text=f"{icon} {message}", font=('Arial', 10, 'bold'),
                        bg='#2a3a2a', fg='#FFD700', wraplength=310, justify='left')
        label.pack()
        
        # Вычисляем высоту
        self.window.update_idletasks()
        label_height = label.winfo_reqheight()
        self.height = label_height + 30
        self.window.geometry(f"350x{self.height}")
        
        # ✅ ИСПРАВЛЕНО: позиционируем внутри контейнера (в левом верхнем углу)
        container_x = self.manager.container.winfo_x()
        container_y = self.manager.container.winfo_y()
        self.window.geometry(f"+{container_x}+{container_y}")
        
        # Плавное появление
        self.fade_in()
        
        # Запускаем таймер на исчезновение
        self.window.after(duration, self.start_fade_out)
    
    def get_height(self):
        """Возвращает высоту уведомления"""
        return self.height
    
    def move_to(self, y_offset):
        """Перемещает уведомление на указанную позицию (снизу)"""
        try:
            if self._destroyed or self.window is None:
                return
            if not self.window.winfo_exists():
                return
                
            # Получаем позицию контейнера
            container_x = self.manager.container.winfo_x()
            container_y = self.manager.container.winfo_y()
            container_height = self.manager.container.winfo_height()
            
            # ✅ ИСПРАВЛЕНО: вычисляем позицию ОТ НИЗА контейнера
            y = container_y + container_height - self.height - y_offset - 10
            if y < container_y:
                y = container_y
            
            # Используем geometry для перемещения
            self.window.geometry(f"350x{self.height}+{container_x}+{y}")
        except (tk.TclError, AttributeError):
            pass
    
    def is_valid(self):
        """Проверяет, существует ли окно"""
        try:
            return self.window is not None and self.window.winfo_exists()
        except:
            return False
    
    def fade_in(self):
        """Плавное появление"""
        if self._destroyed or self.window is None:
            return
        try:
            if not self.window.winfo_exists():
                return
        except:
            return
            
        alpha = 0.0
        step = 0.05
        
        def do_fade():
            nonlocal alpha
            if self._destroyed:
                return
            try:
                if not self.window.winfo_exists():
                    self._destroyed = True
                    return
            except:
                self._destroyed = True
                return
                
            alpha += step
            if alpha >= 0.95:
                try:
                    self.window.attributes('-alpha', 0.95)
                except:
                    pass
                return
            try:
                self.window.attributes('-alpha', alpha)
                self.window.after(30, do_fade)
            except:
                self._destroyed = True
        
        do_fade()
    
    def start_fade_out(self):
        """Начинает плавное исчезновение"""
        if self._destroyed:
            return
        self._fading = True
        self.fade_out(0.95)
    
    def fade_out(self, alpha):
        """Плавное исчезновение"""
        if self._destroyed:
            return
        
        try:
            if not self.window.winfo_exists():
                self._destroyed = True
                return
        except:
            self._destroyed = True
            return
        
        if alpha > 0:
            alpha -= 0.05
            try:
                self.window.attributes('-alpha', alpha)
                self.window.after(30, lambda: self.fade_out(alpha))
            except (tk.TclError, AttributeError):
                self._destroyed = True
        else:
            self.close()
    
    def close(self):
        """Принудительно закрывает уведомление"""
        if self._destroyed:
            return
        self._destroyed = True
        try:
            if self.window and self.window.winfo_exists():
                self.window.destroy()
        except:
            pass
        self.window = None
        self.manager.remove_toast(self)

class Horse:
    def __init__(self, level: int, name: str, owner_color: str, is_temp: bool = False):
        self.level = level
        self.name = name
        self.owner_color = owner_color
        self.is_temp = is_temp
        self.upgrades = []
        self.upgrade_count = 0
        self.training_progress = 0
        self.weekly_training_gain = 0
        self.pending_upgrades = 0
        self.temp_task_type = None
        self.start_of_week_pending = 0
        
        # ✅ Берем данные из глобальной структуры
        level_data = HORSE_LEVELS.get(level, HORSE_LEVELS[1])
        self.base_food = level_data['base_food']
        self.base_water = level_data['base_water']
        self.base_speed = level_data['base_speed']
        self.cost = level_data['cost']
        self.icon = level_data['icon']
    
    @property
    def food_per_day(self):
        radish_upgrades = sum(1 for u in self.upgrades if u == 'radish')
        return max(0, self.base_food - radish_upgrades)
    
    @property
    def water_per_day(self):
        water_upgrades = sum(1 for u in self.upgrades if u == 'water')
        return max(0, self.base_water - water_upgrades)
    
    @property
    def total_speed(self):
        speed_upgrades = sum(1 for u in self.upgrades if u == 'speed')
        return self.base_speed + speed_upgrades
    
    def feed_cost(self):
        return self.food_per_day, self.water_per_day
    
    def sell_price(self):
        base_price = self.cost
        # За каждую цветную прокачку (speed, radish, water) +1 золотая (4 четвертака)
        color_upgrades = len(self.upgrades)  # speed, radish, water
        # За каждую белую прокачку (pending) +1 четвертак
        white_upgrades = self.pending_upgrades
        
        return base_price + (color_upgrades * QUARTERS_PER_GOLD) + white_upgrades
    
    def get_upgrade_display(self):
        display = []
        for i in range(len(self.upgrades)):
            display.append(self.upgrades[i])
        for i in range(self.pending_upgrades):
            display.append('pending')
        remaining = TRAINING_UPGRADES_MAX - len(display)
        for i in range(remaining):
            display.append('empty')
        return display[:TRAINING_UPGRADES_MAX]
    
    def get_upgrade_emojis(self):
        display = self.get_upgrade_display()
        emojis = []
        for u in display:
            if u == 'speed':
                emojis.append('🔴')
            elif u == 'radish':
                emojis.append('🟢')
            elif u == 'water':
                emojis.append('🔵')
            elif u == 'pending':
                emojis.append('⚪')
            else:
                emojis.append('⚫')
        return ''.join(emojis)

class TempHorse:
    def __init__(self, horse, task_type, advance, reward_on_complete, owner_name, weekly_cost):
        self.horse = horse
        self.task_type = task_type
        self.advance = advance
        self.reward_on_complete = reward_on_complete
        self.owner_name = owner_name
        self.weeks_left = 1
        self.completed = False
        self.weekly_cost = weekly_cost
        self.advance_paid = False
        self.horse.temp_task_type = task_type
        self.race_won = False 
        self.race_participated = False
        self.race_skipped_by_owner = False 
        self.start_pending_upgrades = horse.pending_upgrades
        self.original_horse = None  # ✅ Ссылка на оригинальную лошадь у владельца
        self.owner = None           # ✅ Ссылка на владельца

class HorseOwner:
    def __init__(self, name: str, color: str = "#888888", wealth: int = 2):
        self.name = name
        self.color = color  # Цвет для отображения
        self.wealth = wealth  # Уровень богатства (1-4)
        self.horses = []  # Все лошади фермера
        self.horses_for_sale = []  # Лошади на продажу (макс 4)
        self.money = wealth * 10 * QUARTERS_PER_GOLD  # Капитал зависит от богатства
        self.max_sale_horses = 4  # Максимум лошадей на продажу

class Player:
    def __init__(self, name: str, color: str, is_bot: bool = False, order: int = 0, game=None):
        self.name = name
        self.color = color
        self.is_bot = is_bot
        self.order = order
        self.game = game  # Сохраняем ссылку на игру
        self.gold_quarters = 5 * QUARTERS_PER_GOLD
        self.stables = 1
        self.fields = 0
        self.horses = []
        self.water_buckets = 4
        self.radishes = 4
        self.land_map = [0] * MAX_LAND
        self.land_map[0] = 1
        self.horse_positions = {}
        self.radish_positions = {}
        self.action_taken = False
        self.temp_horse = None
        self.is_bankrupt = False
        
        if game:
            start_horse = Horse(1, game.get_unique_horse_name(), color, False)
            self.horses.append(start_horse)
            self.horse_positions[0] = 0
    
    @property
    def total_capital(self):
        if self.is_bankrupt:
            return 0
        capital = self.gold_quarters
        capital += self.radishes * PRICE_RADISH
        capital += self.water_buckets * PRICE_WATER
        capital += self.stables * PRICE_STABLE
        capital += self.fields * PRICE_FIELD
        for h in self.horses:
            if not h.is_temp:
                capital += h.sell_price()
        # ✅ Если капитал отрицательный, возвращаем его как есть
        return capital
        
    def apply_cursor_to_all_buttons(self, parent):
        """Рекурсивно применяет курсор ко всем кнопкам"""
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(cursor="hand2")
            else:
                self.apply_cursor_to_all_buttons(widget)

    def get_free_stable(self):
        for i in range(MAX_LAND):
            if self.land_map[i] == 1 and i not in self.horse_positions:
                return i
        return -1
    
    def get_free_fields(self):
        return [i for i in range(MAX_LAND) if self.land_map[i] == 2 and i not in self.radish_positions]
    
    def add_stable(self, count=1):
        added = 0
        for _ in range(count):
            for i in range(MAX_LAND):
                if self.land_map[i] == 0:
                    self.land_map[i] = 1
                    self.stables += 1
                    added += 1
                    break
            if added >= count:
                break
        return added
    
    def add_field(self, count=1):
        added = 0
        for _ in range(count):
            for i in range(MAX_LAND):
                if self.land_map[i] == 0:
                    self.land_map[i] = 2
                    self.fields += 1
                    added += 1
                    break
            if added >= count:
                break
        return added
    
    def remove_stable(self, position):
        if position < len(self.land_map) and self.land_map[position] == 1 and position not in self.horse_positions:
            self.land_map[position] = 0
            self.stables -= 1
            return True
        return False
    
    def remove_field(self, position):
        if position < len(self.land_map) and self.land_map[position] == 2:
            if position in self.radish_positions:
                del self.radish_positions[position]
            self.land_map[position] = 0
            self.fields -= 1
            return True
        return False
    
    def feed_horses_with_choice(self, game):
        """
        Кормление лошадей с выбором, кого кормить
        Возвращает (все_сыты, сообщение, список_погибших)
        """
        total_radish_need = sum(h.food_per_day for h in self.horses)
        total_water_need = sum(h.water_per_day for h in self.horses)
        
        # Если ресурсов хватает на всех - кормим всех
        if self.radishes >= total_radish_need and self.water_buckets >= total_water_need:
            self.radishes -= total_radish_need
            self.water_buckets -= total_water_need
            return True, f"✅ {self.name}: все лошади сыты", []
        
        # ДЛЯ БОТОВ - АВТОМАТИЧЕСКИЙ ВЫБОР (без диалога)
        if self.is_bot:
            # Бот кормит лошадей пока хватает ресурсов (случайный порядок)
            fed_horses = []
            starved_horses = []
            
            # Копируем список лошадей для случайного порядка
            horses_copy = self.horses.copy()
            random.shuffle(horses_copy)
            
            radishes_left = self.radishes
            water_left = self.water_buckets
            
            for horse in horses_copy:
                need_food = horse.food_per_day
                need_water = horse.water_per_day
                
                if radishes_left >= need_food and water_left >= need_water:
                    fed_horses.append(horse)
                    radishes_left -= need_food
                    water_left -= need_water
                else:
                    starved_horses.append(horse)
            
            # Списываем ресурсы
            total_food = sum(h.food_per_day for h in fed_horses)
            total_water = sum(h.water_per_day for h in fed_horses)
            self.radishes -= total_food
            self.water_buckets -= total_water
            
            # Обрабатываем погибших лошадей
            dead_own = []
            dead_temp = []
            
            for horse in starved_horses:
                if horse.is_temp:
                    dead_temp.append(horse)
                else:
                    dead_own.append(horse)
            
            # Штраф за временных лошадей (для ботов)
            penalty = 0
            horse_cost = 0
            if dead_temp and self.temp_horse:
                if self.temp_horse.advance_paid:
                    penalty = self.temp_horse.advance
                    self.gold_quarters -= penalty
                
                horse_cost = self.temp_horse.horse.sell_price()
                self.gold_quarters -= horse_cost
                
                # ✅ УБИРАЕМ ОГРАНИЧЕНИЕ - игрок может уйти в минус
                # if self.gold_quarters < 0:
                #     self.gold_quarters = 0
            
            # Сохраняем соответствие позиция -> лошадь
            pos_to_horse = {pos: self.horses[idx] for pos, idx in self.horse_positions.items()}
            
            # Удаляем погибших лошадей
            for horse in starved_horses:
                self.horses.remove(horse)
            
            # Перестраиваем horse_positions заново
            self.horse_positions = {}
            for pos, horse in pos_to_horse.items():
                if horse in self.horses:
                    new_idx = self.horses.index(horse)
                    self.horse_positions[pos] = new_idx
            
            # ВОСКРЕШАЕМ УМЕРШИХ ЛОШАДЕЙ (ПОСЛЕ УДАЛЕНИЯ)
            for horse in starved_horses:
                horse_name = horse.name
                horse_level = horse.level
                was_temp = horse.is_temp
                game.resurrect_horse_to_farmer(horse_name, horse_level, was_temp)
            
            # Если погибла временная лошадь, удаляем задание
            if dead_temp:
                self.temp_horse = None
            
            # Формируем сообщение
            msg = f"🍽️ {self.name}: "
            if fed_horses:
                msg += f"накормлены: {', '.join(h.name for h in fed_horses)}. "
            if starved_horses:
                msg += f"погибли: {', '.join(h.name for h in starved_horses)}. "
            if penalty > 0:
                penalty_gold = penalty // QUARTERS_PER_GOLD
                penalty_q = penalty % QUARTERS_PER_GOLD
                msg += f"Штраф за опеку: {penalty_gold}.{penalty_q} зол."
            if horse_cost > 0:
                horse_cost_gold = horse_cost // QUARTERS_PER_GOLD
                horse_cost_q = horse_cost % QUARTERS_PER_GOLD
                msg += f" Убыток от смерти лошади: {horse_cost_gold}.{horse_cost_q} зол."
            
            return len(starved_horses) == 0, msg, starved_horses
        
        # ДЛЯ ЛЮДЕЙ - ПОКАЗЫВАЕМ ДИАЛОГ
        # Если ресурсов не хватает - показываем диалог выбора
        dialog = tk.Toplevel(game.root)
        dialog.title("🐴 ВЫБОР КОРМЛЕНИЯ")
        dialog.geometry("950x500")
        dialog.configure(bg='#2a3a2a')
        dialog.transient(game.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"У {self.name} не хватает ресурсов на всех лошадей!", 
                font=('Arial', 14, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        tk.Label(dialog, text=f"🥕 Редисок: {self.radishes} | 💧 Воды: {self.water_buckets}", 
                font=('Arial', 12), bg='#2a3a2a', fg='white').pack(pady=5)
        
        tk.Label(dialog, text="Выберите лошадей, которых хотите накормить:", 
                font=('Arial', 12), bg='#2a3a2a', fg='white').pack(pady=10)
        
        # Canvas для прокрутки
        canvas = tk.Canvas(dialog, bg='#2a3a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a3a2a')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Создаём чекбоксы для каждой лошади
        horse_vars = []
        
        for i, horse in enumerate(self.horses):
            need_food = horse.food_per_day
            need_water = horse.water_per_day
            
            var = tk.BooleanVar(value=True)  # По умолчанию выбраны все
            horse_vars.append((var, horse, i))
            
            frame = tk.Frame(scrollable_frame, bg='#3a4a3a', relief='ridge', bd=2)
            frame.pack(fill='x', pady=5, padx=10)
            
            cb = tk.Checkbutton(frame, variable=var, bg='#3a4a3a', selectcolor='#4a7a2e', 
                               activebackground='#4a7a2e', fg='white')
            cb.pack(side='left', padx=10)
            
            temp_mark = "🔵 (ОПЕКА) " if horse.is_temp else "🟤 "
            info = f"{temp_mark}{horse.icon} {horse.name} (Ур.{horse.level}) | 🥕 {need_food} | 💧 {need_water}"
            tk.Label(frame, text=info, font=('Arial', 11), bg='#3a4a3a', fg='white').pack(side='left', padx=10)
        
        result = [None]  # Используем список для изменяемой переменной
        
        def confirm():
            selected = []  # ЛОКАЛЬНАЯ ПЕРЕМЕННАЯ ВНУТРИ ФУНКЦИИ
            total_food = 0
            total_water = 0
            
            for var, horse, idx in horse_vars:
                if var.get():
                    selected.append(horse)
                    total_food += horse.food_per_day
                    total_water += horse.water_per_day
            
            if total_food > self.radishes or total_water > self.water_buckets:
                game.show_message("Ошибка", "Не хватает ресурсов для выбранных лошадей!", "warning")
                return
            
            result[0] = selected  # Сохраняем результат
            dialog.destroy()
        
        def skip_feed():
            result[0] = []  # Не кормим никого
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg='#2a3a2a')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="КОРМИТЬ ВЫБРАННЫХ", command=confirm,
                 bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=8).pack(side='left', padx=15)
        
        tk.Button(btn_frame, text="НЕ КОРМИТЬ НИКОГО", command=skip_feed,
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=8).pack(side='left', padx=15)
        
        game.root.wait_window(dialog)
        
        # Получаем выбранных лошадей из result
        selected_horses = result[0] if result[0] is not None else []
        
        # Кормим выбранных лошадей
        fed_horses = []
        starved_horses = []

        for horse in self.horses:
            if horse in selected_horses:
                fed_horses.append(horse)
            else:
                starved_horses.append(horse)

        # Списываем ресурсы
        total_food = sum(h.food_per_day for h in fed_horses)
        total_water = sum(h.water_per_day for h in fed_horses)
        self.radishes -= total_food
        self.water_buckets -= total_water

        # Обрабатываем погибших лошадей
        dead_own = []
        dead_temp = []

        for horse in starved_horses:
            if horse.is_temp:
                dead_temp.append(horse)
            else:
                dead_own.append(horse)

        # Штраф за временных лошадей
        penalty = 0
        horse_cost = 0
        if dead_temp and self.temp_horse:
            # Штраф за провал задания (аванс)
            if self.temp_horse.advance_paid:
                penalty = self.temp_horse.advance
                self.gold_quarters -= penalty
            
            # Стоимость лошади (вычитается отдельно)
            horse_cost = self.temp_horse.horse.sell_price()
            self.gold_quarters -= horse_cost
            
            # ✅ УБИРАЕМ ОГРАНИЧЕНИЕ - игрок может уйти в минус
            # if self.gold_quarters < 0:
            #     self.gold_quarters = 0

        # Сохраняем соответствие позиция -> лошадь
        pos_to_horse = {pos: self.horses[idx] for pos, idx in self.horse_positions.items()}

        # Удаляем погибших лошадей
        for horse in starved_horses:
            self.horses.remove(horse)

        # Перестраиваем horse_positions заново
        self.horse_positions = {}
        for pos, horse in pos_to_horse.items():
            if horse in self.horses:
                new_idx = self.horses.index(horse)
                self.horse_positions[pos] = new_idx

        # ВОСКРЕШАЕМ УМЕРШИХ ЛОШАДЕЙ (ПОСЛЕ УДАЛЕНИЯ)
        for horse in starved_horses:
            horse_name = horse.name
            horse_level = horse.level
            was_temp = horse.is_temp
            game.resurrect_horse_to_farmer(horse_name, horse_level, was_temp)

        # Если погибла временная лошадь, удаляем задание
        if dead_temp:
            self.temp_horse = None

        # Формируем сообщение
        msg = f"🍽️ {self.name}: "
        if fed_horses:
            msg += f"накормлены: {', '.join(h.name for h in fed_horses)}. "
        if starved_horses:
            msg += f"погибли: {', '.join(h.name for h in starved_horses)}. "
        if penalty > 0:
            penalty_gold = penalty // QUARTERS_PER_GOLD
            penalty_q = penalty % QUARTERS_PER_GOLD
            if penalty_q > 0:
                msg += f"Штраф за опеку: {penalty_gold}.{penalty_q} зол."
            else:
                msg += f"Штраф за опеку: {penalty_gold} зол."
        if horse_cost > 0:
            horse_cost_gold = horse_cost // QUARTERS_PER_GOLD
            horse_cost_q = horse_cost % QUARTERS_PER_GOLD
            if horse_cost_q > 0:
                msg += f" Убыток от смерти лошади: {horse_cost_gold}.{horse_cost_q} зол."
            else:
                msg += f" Убыток от смерти лошади: {horse_cost_gold} зол."

        return len(starved_horses) == 0, msg, starved_horses

    def plant_radishes(self, field_pos, count):
        if field_pos not in self.radish_positions:
            self.radish_positions[field_pos] = []
        
        available = RADISH_PER_FIELD - len(self.radish_positions[field_pos])
        plant = min(count, available, self.radishes, self.water_buckets)
        
        if plant > 0:
            self.water_buckets -= plant
            self.radishes -= plant
            for i in range(plant):
                self.radish_positions[field_pos].append(i)
            return plant
        return 0

class NumericDialog(tk.Toplevel):
    """Диалог для выбора числа от 0 до максимума"""
    def __init__(self, parent, title, prompt, max_value, default=0, sound_manager=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x400")
        self.configure(bg='#2a3a2a')
        self.transient(parent)
        self.grab_set()

        self.sound = sound_manager
        self.result = None
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"+{x}+{y}")
        
        tk.Label(self, text=prompt, font=('Arial', 14, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=20)
        
        spinbox_frame = tk.Frame(self, bg='#2a3a2a')
        spinbox_frame.pack(pady=10)
        
        self.value_var = tk.IntVar(value=default)
        self.spinbox = tk.Spinbox(spinbox_frame, from_=0, to=max_value, textvariable=self.value_var,
                                   width=5, font=('Arial', 14))
        self.spinbox.pack(side='left', padx=10)
        
        # Текстовое представление
        self.value_label = tk.Label(spinbox_frame, text=self.get_text(default), font=('Arial', 14),
                                    bg='#2a3a2a', fg='white')
        self.value_label.pack(side='left', padx=10)
        
        def update_label(*args):
            val = self.value_var.get()
            self.value_label.config(text=self.get_text(val))
        
        # ✅ ИСПРАВЛЕНО: используем trace_add вместо trace
        self.value_var.trace_add('write', lambda *args: update_label())
        
        btn_frame = tk.Frame(self, bg='#2a3a2a')
        btn_frame.pack(pady=30)
        
        ok_btn = self.create_styled_button(btn_frame, "ПОДТВЕРДИТЬ", self.ok, '#4a7a2e')
        ok_btn.pack(side='left', padx=15)
        
        cancel_btn = self.create_styled_button(btn_frame, "ОТМЕНА", self.cancel, '#8B4513')
        cancel_btn.pack(side='left', padx=15)
        self.apply_hover_to_buttons()

    def apply_hover_to_buttons(self):
        """Применяет подсветку ко всем кнопкам в диалоге"""
        def apply_recursive(widget):
            if isinstance(widget, tk.Button):
                original_bg = widget.cget('bg')
                if original_bg == '#4a7a2e':
                    hover_color = '#5a9a3e'
                elif original_bg == '#8B4513':
                    hover_color = '#a06030'
                else:
                    hover_color = original_bg
                
                def on_enter(e, btn=widget, color=hover_color):
                    btn.config(bg=color, cursor="hand2")
                
                def on_leave(e, btn=widget, color=original_bg):
                    btn.config(bg=color)
                
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.config(cursor="hand2")
            
            for child in widget.winfo_children():
                apply_recursive(child)
        
        apply_recursive(self)
    
    def get_text(self, value):
        """Возвращает текстовое представление числа"""
        if value == 0:
            return "0 ботов"
        elif value == 1:
            return "1 бот"
        elif 2 <= value <= 4:
            return f"{value} бота"
        else:
            return f"{value} ботов"
    
    def create_styled_button(self, parent, text, command, color):
        """Создаёт стилизованную кнопку"""
        hover_color = '#5a9a3e' if color == '#4a7a2e' else '#a06030'
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg='white', font=('Arial', 12, 'bold'), 
                       padx=25, pady=5, cursor="hand2",
                       activebackground=hover_color, activeforeground='white')
        
        def on_enter(e):
            btn.config(bg=hover_color)
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def ok(self):
        if self.sound:
            self.sound.play('click')
        self.result = self.value_var.get()
        self.destroy()
    
    def cancel(self):
        if self.sound:
            self.sound.play('click')
        self.result = None
        self.destroy()

class StyledDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, options, default=0, sound_manager=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x400")
        self.configure(bg='#2a3a2a')
        self.transient(parent)
        self.grab_set()

        self.sound = sound_manager
        self.result = None
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"+{x}+{y}")
        
        tk.Label(self, text=prompt, font=('Arial', 14, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=20)
        
        spinbox_frame = tk.Frame(self, bg='#2a3a2a')
        spinbox_frame.pack(pady=10)
        
        self.value_var = tk.IntVar(value=default + 1)
        self.spinbox = tk.Spinbox(spinbox_frame, from_=1, to=len(options), textvariable=self.value_var,
                                   width=5, font=('Arial', 14))
        self.spinbox.pack(side='left', padx=10)
        
        self.value_label = tk.Label(spinbox_frame, text=options[default], font=('Arial', 14),
                                    bg='#2a3a2a', fg='white')
        self.value_label.pack(side='left', padx=10)
        
        def update_label(*args):
            idx = self.value_var.get() - 1
            if 0 <= idx < len(options):
                self.value_label.config(text=options[idx])
        
        # ✅ ИСПРАВЛЕНО: используем trace_add вместо trace
        self.value_var.trace_add('write', lambda *args: update_label())
        update_label()
        
        btn_frame = tk.Frame(self, bg='#2a3a2a')
        btn_frame.pack(pady=30)
        
        ok_btn = self.create_styled_button(btn_frame, "ПОДТВЕРДИТЬ", self.ok, '#4a7a2e')
        ok_btn.pack(side='left', padx=15)
        
        cancel_btn = self.create_styled_button(btn_frame, "ОТМЕНА", self.cancel, '#8B4513')
        cancel_btn.pack(side='left', padx=15)
        self.apply_hover_to_buttons()

    def apply_hover_to_buttons(self):
        """Применяет подсветку ко всем кнопкам в диалоге"""
        def apply_recursive(widget):
            if isinstance(widget, tk.Button):
                original_bg = widget.cget('bg')
                if original_bg == '#4a7a2e':
                    hover_color = '#5a9a3e'
                elif original_bg == '#8B4513':
                    hover_color = '#a06030'
                else:
                    hover_color = original_bg
                
                def on_enter(e, btn=widget, color=hover_color):
                    btn.config(bg=color, cursor="hand2")
                
                def on_leave(e, btn=widget, color=original_bg):
                    btn.config(bg=color)
                
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.config(cursor="hand2")
            
            for child in widget.winfo_children():
                apply_recursive(child)
        
        apply_recursive(self)
    
    def create_styled_button(self, parent, text, command, color):
        """Создаёт стилизованную кнопку"""
        hover_color = '#5a9a3e' if color == '#4a7a2e' else '#a06030'
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg='white', font=('Arial', 12, 'bold'), 
                       padx=25, pady=5, cursor="hand2",
                       activebackground=hover_color, activeforeground='white')
        
        def on_enter(e):
            btn.config(bg=hover_color)
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def ok(self):
        if self.sound:
            self.sound.play('click')
        self.result = self.value_var.get() - 1  # Возвращаем индекс (0, 1, 2...)
        self.destroy()
    
    def cancel(self):
        if self.sound:
            self.sound.play('click')
        self.result = None
        self.destroy()

class LotteryDialog(tk.Toplevel):
    def __init__(self, parent, max_tickets, sound_manager):
        super().__init__(parent)
        self.title("🎰 ЛОТЕРЕЯ")
        self.geometry("450x350")
        self.configure(bg='#2a3a2a')
        self.transient(parent)
        self.grab_set()

        self.sound = sound_manager
        self.result = None
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (350 // 2)
        self.geometry(f"+{x}+{y}")
        
        tk.Label(self, text="🎰 ЛОТЕРЕЯ 🎰", font=('Arial', 20, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=20)
        
        tk.Label(self, text=f"Доступно билетов: {max_tickets}", font=('Arial', 14),
                bg='#2a3a2a', fg='white').pack(pady=10)
        
        tk.Label(self, text="Выберите количество билетов:", font=('Arial', 12),
                bg='#2a3a2a', fg='white').pack(pady=10)
        
        self.ticket_var = tk.IntVar(value=1)
        ticket_spinbox = tk.Spinbox(self, from_=1, to=max_tickets, textvariable=self.ticket_var,
                                     width=10, font=('Arial', 14))
        ticket_spinbox.pack(pady=10)
        
        btn_frame = tk.Frame(self, bg='#2a3a2a')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="КУПИТЬ БИЛЕТЫ", command=self.ok,
                 bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=5).pack(side='left', padx=15)
        tk.Button(btn_frame, text="ОТМЕНА", command=self.cancel,
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=5).pack(side='left', padx=15)
        self.apply_hover_to_buttons()

    def apply_hover_to_buttons(self):
        """Применяет подсветку ко всем кнопкам в диалоге"""
        def apply_recursive(widget):
            if isinstance(widget, tk.Button):
                original_bg = widget.cget('bg')
                if original_bg == '#4a7a2e':
                    hover_color = '#5a9a3e'
                elif original_bg == '#8B4513':
                    hover_color = '#a06030'
                else:
                    hover_color = original_bg
                
                def on_enter(e, btn=widget, color=hover_color):
                    btn.config(bg=color, cursor="hand2")
                
                def on_leave(e, btn=widget, color=original_bg):
                    btn.config(bg=color)
                
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.config(cursor="hand2")
            
            for child in widget.winfo_children():
                apply_recursive(child)
        
        apply_recursive(self)

    def ok(self):
        if self.sound:
            self.sound.play('click')
        self.result = self.ticket_var.get()
        self.destroy()
    
    def cancel(self):
        if self.sound:
            self.sound.play('click')
        self.destroy()

class PlantDialog(tk.Toplevel):
    def __init__(self, parent, field_pos, max_plant, player_name, sound_manager, callback):
        super().__init__(parent)
        self.title("🌱 ПОСАДКА РЕДИСОК")
        self.geometry("400x350")
        self.configure(bg='#2a3a2a')
        self.transient(parent)
        self.grab_set()

        self.sound = sound_manager
        self.field_pos = field_pos
        self.max_plant = max_plant
        self.callback = callback
        self.result = None
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (350 // 2)
        self.geometry(f"+{x}+{y}")
        
        tk.Label(self, text="🌱 ПОСАДКА РЕДИСОК 🌱", font=('Arial', 16, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        tk.Label(self, text=f"Поле №{field_pos + 1}", font=('Arial', 12),
                bg='#2a3a2a', fg='white').pack(pady=5)
        
        tk.Label(self, text=f"Максимум редисок: {max_plant}/4", font=('Arial', 12),
                bg='#2a3a2a', fg='white').pack(pady=5)
        
        tk.Label(self, text="Выберите количество редисок для посадки:", font=('Arial', 12),
                bg='#2a3a2a', fg='white').pack(pady=10)
        
        self.plant_var = tk.IntVar(value=1)
        plant_spinbox = tk.Spinbox(self, from_=1, to=max_plant, textvariable=self.plant_var,
                                    width=10, font=('Arial', 14))
        plant_spinbox.pack(pady=10)
        
        btn_frame = tk.Frame(self, bg='#2a3a2a')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="ПОСАДИТЬ", command=self.ok,
                 bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=5).pack(side='left', padx=15)
        tk.Button(btn_frame, text="ОТМЕНА", command=self.cancel,
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=5).pack(side='left', padx=15)

        self.apply_hover_to_buttons()

    def apply_hover_to_buttons(self):
        """Применяет подсветку ко всем кнопкам в диалоге"""
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                original_bg = widget.cget('bg')
                if original_bg == '#4a7a2e':
                    hover_color = '#5a9a3e'
                elif original_bg == '#8B4513':
                    hover_color = '#a06030'
                else:
                    hover_color = original_bg
                
                def on_enter(e, btn=widget, color=hover_color):
                    btn.config(bg=color, cursor="hand2")
                
                def on_leave(e, btn=widget, color=original_bg):
                    btn.config(bg=color)
                
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.config(cursor="hand2")
    
    def ok(self):
        if self.sound:
            self.sound.play('click')
        self.result = self.plant_var.get()
        self.callback(self.field_pos, self.result)
        self.destroy()
    
    def cancel(self):
        if self.sound:
            self.sound.play('click')
        self.destroy()

class RaceDialog(tk.Toplevel):
    def __init__(self, parent, participants, sound_manager, callback):
        super().__init__(parent)
        self.title("🏇 СКАЧКИ")
        self.geometry("900x700")
        self.configure(bg='#2a3a2a')
        self.transient(parent)
        self.grab_set()

        self.sound = sound_manager
        self.participants = participants
        self.callback = callback
        self.race_canvas = None
        self.horses_on_track = []
        self.y_positions = []
        self.finished_count = 0
        self.results = []
        self.race_in_progress = False
        self.animation_id = None
        self._shoot_called = False
        
        self.countdown_label = None
        self.countdown_value = 0
        self.countdown_timer_id = None
        self.update_timer_id = None

        self.horse_images = {}
        self.load_horse_race_images()

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # 1. Плавное затухание музыки (2 секунды)
        if self.sound:
            self.sound.fade_out_music(2000, 0.0)
            # 2. Ждём затухания, затем звук старта
            self.after(2000, self.play_race_start)
    
    def load_horse_race_images(self):
        """Загружает PNG-изображения для скачек"""
        images_dir = Path(resource_path("horse_images"))
        
        race_image_size = (64, 64)
        
        for level in [1, 2, 3]:
            right_path = images_dir / f"horse_{level}_right.png"
            if right_path.exists():
                try:
                    img = Image.open(right_path).resize(race_image_size, Image.Resampling.LANCZOS)
                    self.horse_images[f"{level}_right"] = ImageTk.PhotoImage(img)
                except:
                    self.horse_images[f"{level}_right"] = None
            else:
                self.horse_images[f"{level}_right"] = None
            
            left_path = images_dir / f"horse_{level}_left.png"
            if left_path.exists():
                try:
                    img = Image.open(left_path).resize(race_image_size, Image.Resampling.LANCZOS)
                    self.horse_images[f"{level}_left"] = ImageTk.PhotoImage(img)
                except:
                    self.horse_images[f"{level}_left"] = None
            else:
                self.horse_images[f"{level}_left"] = None

    def play_race_start(self):
        """Воспроизводит звук начала скачек"""
        if self.sound:
            # Создаём метку для отображения
            self.countdown_label = tk.Label(self, text="", font=('Arial', 64, 'bold'),
                                             bg='#2a3a2a', fg='#FFD700')
            self.countdown_label.pack(pady=10)
            
            # Запускаем мигание тройки
            self.blinking = True
            self.blink_count = 0
            self.start_blinking_three()
            
            # Воспроизводим звук
            self.sound.play('race_start')
            
            # Получаем длительность звука
            duration = self.sound.get_sound_length('race_start')
            
            # Запускаем обратный отсчёт за 3 секунды до окончания звука
            delay = max(0, duration - 3000)
            self.after(delay, self.start_full_countdown)
            
            # Ждём окончания звука
            self.after(duration, self.on_race_start_finished)
        else:
            self.play_shoot_sound()

    def start_blinking_three(self):
        """Запускает мигание тройки"""
        if not hasattr(self, 'blinking') or not self.blinking:
            return
        
        if self.blink_count < 6:  # 6 морганий (3 секунды)
            if self.blink_count % 2 == 0:
                self.countdown_label.config(text="3", font=('Arial', 72, 'bold'), fg='#FFD700')
            else:
                self.countdown_label.config(text="")
            
            self.blink_count += 1
            self.after(500, self.start_blinking_three)
        else:
            self.countdown_label.config(text="3", font=('Arial', 72, 'bold'), fg='#FFD700')

    def start_full_countdown(self):
        """Запускает полный обратный отсчёт 3-2-1-СТАРТ! (без мигания)"""
        # Останавливаем мигание
        self.blinking = False
        
        # Сбрасываем счётчик для отсчёта
        self.countdown_value = 3
        self.do_countdown_step()

    def do_countdown_step(self):
        """Выполняет один шаг обратного отсчёта без мигания"""
        if not hasattr(self, 'countdown_label') or self.countdown_label is None:
            return
        
        if self.countdown_value > 0:
            # Показываем цифру
            self.countdown_label.config(text=str(self.countdown_value), 
                                       font=('Arial', 72, 'bold'), fg='#FFD700')
            # Через 1 секунду переходим к следующей цифре
            self.after(1000, self.next_countdown)
        elif self.countdown_value == 0:
            # Показываем "СТАРТ!"
            self.countdown_label.config(text="СТАРТ!", font=('Arial', 48, 'bold'), fg='#00FF00')
            self.countdown_value = -1
            # "СТАРТ!" останется до выстрела

    def next_countdown(self):
        """Переход к следующей цифре отсчёта"""
        self.countdown_value -= 1
        if self.countdown_value >= 0:
            self.do_countdown_step()

    def on_race_start_finished(self):
        """Вызывается после окончания звука race_start"""
        # Если отсчёт ещё не дошёл до "СТАРТ!", принудительно показываем его
        if self.countdown_value != -1:
            self.countdown_label.config(text="СТАРТ!", font=('Arial', 48, 'bold'), fg='#00FF00')
            self.countdown_value = -1
        
        # Через небольшую задержку стреляем
        self.after(500, self.finish_and_shoot)

    def finish_and_shoot(self):
        """Завершает и переходит к выстрелу"""
        if hasattr(self, 'countdown_label') and self.countdown_label:
            try:
                self.countdown_label.destroy()
            except:
                pass
            self.countdown_label = None
        
        self.play_shoot_sound()

    def play_shoot_sound(self):
        if self.sound and self.sound.sfx_enabled:
            self.sound.play('shoot')
            self.sound.play('horses_run', -1)  # Зацикленный звук
        
        self.after(300, self.start_race)


    def apply_hover_to_buttons(self):
        """Применяет подсветку ко всем кнопкам в диалоге"""
        def apply_recursive(widget):
            if isinstance(widget, tk.Button):
                original_bg = widget.cget('bg')
                if original_bg == '#4a7a2e':
                    hover_color = '#5a9a3e'
                elif original_bg == '#8B4513':
                    hover_color = '#a06030'
                else:
                    hover_color = original_bg
                
                def on_enter(e, btn=widget, color=hover_color):
                    btn.config(bg=color, cursor="hand2")
                
                def on_leave(e, btn=widget, color=original_bg):
                    btn.config(bg=color)
                
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.config(cursor="hand2")
            
            for child in widget.winfo_children():
                apply_recursive(child)
        
        apply_recursive(self)
    
    def setup_ui(self):
        tk.Label(self, text="🏇 СКАЧКИ 🏇", font=('Arial', 24, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        # Уменьшаем высоту canvas - для 4 лошадей достаточно 450-500
        self.race_canvas = tk.Canvas(self, bg='#8B7355', height=480, width=800)
        self.race_canvas.pack(pady=20, padx=25)
        
        start_line = 50
        finish_line = 750
        self.race_canvas.create_line(start_line, 20, start_line, 460, fill='#00FF00', width=3)
        self.race_canvas.create_text(start_line - 10, 15, text="СТАРТ", font=('Arial', 9, 'bold'), fill='#00FF00')
        self.race_canvas.create_line(finish_line, 20, finish_line, 460, fill='#FF4444', width=3)
        self.race_canvas.create_text(finish_line + 10, 15, text="ФИНИШ", font=('Arial', 10, 'bold'), fill='#FF4444')
        
        for i, (player, horse) in enumerate(self.participants):
            y = 70 + i * 95  # 4 участника: 70, 165, 260, 355
            self.y_positions.append(y)
            
            self.race_canvas.create_rectangle(start_line-10, y-30, finish_line+10, y+30, fill='#c2a875', outline='#8B7355')
            self.race_canvas.create_line(start_line, y, finish_line, y, fill='white', width=1, dash=(5, 5))
            self.race_canvas.create_text((start_line + finish_line)//2, y-40, text=f"{player.name} - {horse.name} (Ск.{horse.total_speed})", 
                                   font=('Arial', 10), fill='white')
            
            # Используем изображение вместо текста
            img_key = f"{horse.level}_right"
            if self.horse_images.get(img_key):
                horse_obj = self.race_canvas.create_image(start_line, y, image=self.horse_images[img_key], anchor='center')
            else:
                horse_obj = self.race_canvas.create_text(start_line, y, text=horse.icon, font=('Arial', 48))
                
            self.horses_on_track.append([horse_obj, player, horse, start_line, False, horse.level])

    def animate_race(self):
        if not self.race_in_progress:
            return
            
        if self.finished_count < len(self.participants):
            for idx, (horse_obj, player, horse, pos, finished, level) in enumerate(self.horses_on_track):
                if not finished:
                    move = random.randint(1, 6) + horse.total_speed
                    new_pos = min(pos + move, 750)
                    self.horses_on_track[idx][3] = new_pos
                    
                    # Меняем направление в зависимости от движения
                    if move > 0:
                        img_key = f"{level}_right"
                    else:
                        img_key = f"{level}_left"
                    
                    if self.horse_images.get(img_key):
                        self.race_canvas.itemconfig(horse_obj, image=self.horse_images[img_key])
                    
                    self.race_canvas.coords(horse_obj, new_pos, self.y_positions[idx])
                    
                    if new_pos >= 750 and not finished:
                        self.horses_on_track[idx][4] = True
                        self.finished_count += 1
                        self.results.append((self.finished_count, player, horse))
            
            self.animation_id = self.after(80, self.animate_race)
        else:
            self.finish_race()
    
    def start_race(self):
        self.finished_count = 0
        self.results = []
        self.race_in_progress = True
        self.animate_race()
    
    def finish_race(self):
        self.race_in_progress = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        # Останавливаем звук бега лошадей
        if self.sound:
            self.sound.stop_sound('horses_run')
        
        num_participants = len(self.participants)
        log_messages = []  # Для журнала
        
        # ✅ НОВАЯ СИСТЕМА НАГРАД
        for place, player, horse in self.results:
            reward = 0
            
            if num_participants == 2:
                if place == 1:
                    reward = 2 * QUARTERS_PER_GOLD  # 2 золотых
                # 2-е место - ничего
            elif num_participants == 3:
                if place == 1:
                    reward = 4 * QUARTERS_PER_GOLD  # 4 золотых
                elif place == 2:
                    reward = 2 * QUARTERS_PER_GOLD  # 2 золотых
                # 3-е место - ничего
            elif num_participants >= 4:
                if place == 1:
                    reward = 5 * QUARTERS_PER_GOLD  # 5 золотых
                elif place == 2:
                    reward = 2 * QUARTERS_PER_GOLD + 2  # 2 золотых и 2 четвертака
                elif place == 3:
                    reward = 1 * QUARTERS_PER_GOLD  # 1 золотой
                # 4-е место - ничего
            
            if reward > 0:
                player.gold_quarters += reward
                if reward >= QUARTERS_PER_GOLD:
                    reward_gold = reward // QUARTERS_PER_GOLD
                    reward_q = reward % QUARTERS_PER_GOLD
                    if reward_q > 0:
                        reward_str = f"{reward_gold}.{reward_q} зол."
                    else:
                        reward_str = f"{reward_gold} зол."
                else:
                    reward_str = f"{reward} четвертаков"
                log_messages.append(f"{['🥇','🥈','🥉','📋'][place-1] if place <= 4 else '📋'} {player.name} занял {place} место на {horse.name} (+{reward_str})")
            else:
                log_messages.append(f"{['🥇','🥈','🥉','📋'][place-1] if place <= 4 else '📋'} {player.name} занял {place} место на {horse.name} (без награды)")
            
            # Отмечаем победу для временной лошади (только для 1-го места)
            if place == 1 and player.temp_horse and player.temp_horse.task_type == "win_race" and player.temp_horse.horse.name == horse.name:
                player.temp_horse.race_won = True
        
        # Формируем текст результатов для отображения в диалоге
        result_text = "🏆 РЕЗУЛЬТАТЫ СКАЧЕК 🏆\n\n"
        
        for place, player, horse in self.results[:3]:
            medal = ["🥇", "🥈", "🥉"][place-1] if place <= 3 else "📋"
            
            # Определяем награду для отображения
            if num_participants == 2:
                if place == 1:
                    reward_text = " (+2 зол.)"
                else:
                    reward_text = ""
            elif num_participants == 3:
                if place == 1:
                    reward_text = " (+4 зол.)"
                elif place == 2:
                    reward_text = " (+2 зол.)"
                else:
                    reward_text = ""
            elif num_participants >= 4:
                if place == 1:
                    reward_text = " (+5 зол.)"
                elif place == 2:
                    reward_text = " (+2 зол. 2 четв.)"
                elif place == 3:
                    reward_text = " (+1 зол.)"
                else:
                    reward_text = ""
            else:
                reward_text = ""
            
            result_text += f"{medal} {player.name} - {horse.name}{reward_text}\n"
        
        if len(self.results) > 3:
            result_text += f"\n📋 Остальные:\n"
            for place, player, horse in self.results[3:]:
                result_text += f"   {place}. {player.name} - {horse.name}\n"
        
        # Очищаем canvas и показываем результаты
        self.race_canvas.destroy()
        result_label = tk.Label(self, text=result_text, font=('Arial', 14),
                                bg='#2a3a2a', fg='#FFD700', justify='left')
        result_label.pack(pady=20, padx=20)
        
        if self.sound:
            self.sound.play('race_finish')
        
        # Кнопка закрытия
        tk.Button(self, text="ЗАКРЫТЬ", command=self.close_dialog,
                 bg='#8B4513', fg='white', font=('Arial', 12), padx=25, pady=8).pack(pady=15)
        self.apply_hover_to_buttons()
        
        # Сохраняем информацию для всплывающего сообщения и журнала
        winner_info = f"🏆 ПОБЕДИТЕЛЬ: {self.results[0][1].name} - {self.results[0][2].name}\n"
        if len(self.results) > 1:
            winner_info += f"🥈 2-е место: {self.results[1][1].name} - {self.results[1][2].name}\n"
        if len(self.results) > 2 and num_participants > 2:
            winner_info += f"🥉 3-е место: {self.results[2][1].name} - {self.results[2][2].name}"
        
        self.race_results_info = winner_info
        self.race_log_messages = log_messages
    
    def close_dialog(self):
        if self.sound:
            self.sound.stop_all_sounds()  # Останавливаем ВСЕ звуки
            self.sound.fade_in_music(2000)
            self.sound.play('click')
        
        # Передаём результаты в callback
        if hasattr(self, 'race_log_messages'):
            self.callback(self.race_log_messages)
        else:
            self.callback()
        
        self.destroy()

class SaveLoadDialog(tk.Toplevel):
    def __init__(self, parent, saves_dir, sound_manager, is_load=True):
        super().__init__(parent)
        self.title("📂 ЗАГРУЗКА ИГРЫ" if is_load else "💾 СОХРАНЕНИЕ ИГРЫ")
        self.geometry("550x500")
        self.configure(bg='#2a3a2a')
        self.transient(parent)
        self.grab_set()

        self.sound = sound_manager
        self.saves_dir = saves_dir
        self.is_load = is_load
        self.result = None
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")
        
        tk.Label(self, text="📂 ЗАГРУЗКА СОХРАНЕНИЯ" if is_load else "💾 СОХРАНЕНИЕ ИГРЫ", 
                font=('Arial', 16, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        if is_load:
            saves_frame = tk.Frame(self, bg='#2a3a2a')
            saves_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            tk.Label(saves_frame, text="Доступные сохранения:", font=('Arial', 12),
                    bg='#2a3a2a', fg='white').pack(anchor='w', pady=5)
            
            listbox_frame = tk.Frame(saves_frame, bg='#2a3a2a')
            listbox_frame.pack(fill='both', expand=True)
            
            scrollbar = tk.Scrollbar(listbox_frame)
            scrollbar.pack(side='right', fill='y')
            
            self.saves_listbox = tk.Listbox(listbox_frame, bg='#1a2a1a', fg='white',
                                            font=('Consolas', 10), yscrollcommand=scrollbar.set)
            self.saves_listbox.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=self.saves_listbox.yview)
            
            self.load_saves_list()
            
            btn_frame = tk.Frame(self, bg='#2a3a2a')
            btn_frame.pack(pady=20)
            
            tk.Button(btn_frame, text="ЗАГРУЗИТЬ", command=self.load_selected,
                     bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=25).pack(side='left', padx=15)
            tk.Button(btn_frame, text="ОТМЕНА", command=self.cancel,
                     bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25).pack(side='left', padx=15)
        else:
            save_frame = tk.Frame(self, bg='#2a3a2a')
            save_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            tk.Label(save_frame, text="Введите имя сохранения:", font=('Arial', 12),
                    bg='#2a3a2a', fg='white').pack(anchor='w', pady=5)
            
            self.save_name_entry = tk.Entry(save_frame, width=40, font=('Arial', 12))
            self.save_name_entry.pack(fill='x', pady=5)
            
            default_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.save_name_entry.insert(0, default_name)
            
            tk.Label(save_frame, text=f"Путь сохранения: {self.saves_dir}", font=('Arial', 9),
                    bg='#2a3a2a', fg='gray').pack(pady=10)
            
            btn_frame = tk.Frame(self, bg='#2a3a2a')
            btn_frame.pack(pady=20)

            
            tk.Button(btn_frame, text="СОХРАНИТЬ", command=self.save_game,
                     bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=25).pack(side='left', padx=15)
            tk.Button(btn_frame, text="ОТМЕНА", command=self.cancel,
                     bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25).pack(side='left', padx=15)
        self.apply_hover_to_buttons()

    def apply_hover_to_buttons(self):
        """Применяет подсветку ко всем кнопкам в диалоге"""
        def apply_recursive(widget):
            if isinstance(widget, tk.Button):
                original_bg = widget.cget('bg')
                if original_bg == '#4a7a2e':
                    hover_color = '#5a9a3e'
                elif original_bg == '#8B4513':
                    hover_color = '#a06030'
                else:
                    hover_color = original_bg
                
                def on_enter(e, btn=widget, color=hover_color):
                    btn.config(bg=color, cursor="hand2")
                
                def on_leave(e, btn=widget, color=original_bg):
                    btn.config(bg=color)
                
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.config(cursor="hand2")
            
            for child in widget.winfo_children():
                apply_recursive(child)
        
        apply_recursive(self)
    
    def load_saves_list(self):
        self.saves_listbox.delete(0, tk.END)
        if self.saves_dir.exists():
            saves = list(self.saves_dir.glob("*.json"))
            saves.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for save_file in saves:
                try:
                    with open(save_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        version = data.get('version', 'unknown')
                        day = data.get('current_day', '?')
                        date_str = save_file.stem
                        self.saves_listbox.insert(tk.END, f"{date_str} (День {day}, версия {version})")
                except:
                    self.saves_listbox.insert(tk.END, f"{save_file.stem} (ошибка чтения)")
    
    def load_selected(self):
        if self.saves_listbox.curselection():
            idx = self.saves_listbox.curselection()[0]
            if self.sound:
                self.sound.play('click')
            self.result = idx
            self.destroy()
    
    def save_game(self):
        name = self.save_name_entry.get().strip()
        if name:
            if self.sound:
                self.sound.play('click')
            self.result = name
            self.destroy()
    
    def cancel(self):
        if self.sound:
            self.sound.play('click')
        self.destroy()

class RecordManager:
    def __init__(self):
        self.config_file = Path("records.json")
        self.record_holder = None
        self.record_capital = 0
        self.load_record()
    
    def load_record(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.record_holder = data.get('record_holder', None)
                    self.record_capital = data.get('record_capital', 0)
            except:
                pass
    
    def save_record(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump({
                'record_holder': self.record_holder,
                'record_capital': self.record_capital
            }, f, ensure_ascii=False, indent=2)
    
    def check_and_update_record(self, player):
        if player.total_capital > self.record_capital:
            self.record_holder = player.name
            self.record_capital = player.total_capital
            self.save_record()
            return True
        return False

class HorseBoardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐎 Лошади и Редиски - Фермерская стратегия 🥕")
        
        # ✅ МИНИМАЛЬНЫЙ РАЗМЕР ОКНА (1280x720 - стандарт HD)
        self.MIN_WINDOW_WIDTH = 1280
        self.MIN_WINDOW_HEIGHT = 720
        
        # ✅ ТЕКУЩИЙ РЕЖИМ ОТОБРАЖЕНИЯ
        self.is_fullscreen = True
        
        # ✅ БАЗОВЫЙ РАЗМЕР ДЛЯ РАСЧЁТА МАСШТАБА
        self.BASE_WIDTH = 1920
        self.BASE_HEIGHT = 1080
        
        # ✅ ТЕКУЩИЙ МАСШТАБ (будет обновляться)
        self.current_scale = 1.0
        
        # Устанавливаем начальный размер
        self.root.geometry("1800x1000")
        self.root.state('zoomed')
        self.root.minsize(self.MIN_WINDOW_WIDTH, self.MIN_WINDOW_HEIGHT) 
        
        # ✅ ПРИВЯЗЫВАЕМ ОБРАБОТЧИК ИЗМЕНЕНИЯ РАЗМЕРА
        self.root.bind('<Configure>', self.on_window_resize)
        self.root.bind('<Double-Button-1>', self.on_title_double_click)
        self.root.bind('<Escape>', lambda e: self.toggle_window_size())
        self.root.configure(bg='#1a2a1a')
        
        # ✅ ПОЛУЧАЕМ РАЗМЕР ЭКРАНА (для справки)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # ✅ ВЫЧИСЛЯЕМ НАЧАЛЬНЫЙ МАСШТАБ
        self.update_scale()
        
        # Инициализация остальных переменных
        self.players = []
        self.current_player_idx = 0
        self.current_day = 1
        self.week_number = 1
        self.days_total = 60
        self.warning_shown_today = False
        self.game_active = True
        self.horse_images = {}
        self.horse_gif_frames = []
        self.menu_window = None
        self.race_window = None
        self.race_animating = False
        self.sound = SoundManager()
        self.sound.set_root(root)
        self.game_started = False
        self.race_entries = []
        self.saves_dir = Path("saves")
        self.saves_dir.mkdir(exist_ok=True)
        self.records = RecordManager()
        self.auction_mode = False
        self.race_mode = False
        self.waiting_for_race = False
        self.race_participants = []
        self.race_results = None
        self.event_overlay = None
        self.available_tasks = []
        self.tasks_generated = False
        self.splash_frames = []
        self.splash_label = None
        self.current_splash_frame = 0
        self.used_horse_names = set()
        self.last_race_horse = {}
        self.horse_owners = {}
        self._warning_shown_this_turn = False
        self.toast_manager = ToastManager(root)
        self._resize_timer = None

        # Загрузка ресурсов
        self.init_horse_owners()
        self.distribute_initial_horses()
        self.init_market_horses()
        
        self.load_horse_images()
        self.load_horse_gif()
        
        # ✅ ЗАГРУЖАЕМ ИКОНКУ В САМОМ КОНЦЕ, ПОСЛЕ ВСЕХ ИЗМЕНЕНИЙ ОКНА
        self.load_window_icon()
        
        # ✅ И ЕЩЁ РАЗ ЧЕРЕЗ 500 мс (после создания меню)
        self.root.after(500, self.load_window_icon)
        self.root.after(1000, self.load_window_icon)
        
        self.create_start_menu()
        self.root.protocol("WM_DELETE_WINDOW", self.on_root_close)
    

    def get_screen_category(self):
        """Определяет категорию экрана (для обратной совместимости)"""
        width = self.screen_width
        height = self.screen_height
        
        if width >= 3840 and height >= 2160:
            return "4k"
        elif width >= 2560 and height >= 1440:
            return "2k"
        elif width >= 1920 and height >= 1080:
            return "fullhd"
        elif width >= 1366 and height >= 768:
            return "hd"
        else:
            return "small"

    def scale_size(self, base_size):
        """Масштабирует размер относительно базового Full HD"""
        return int(base_size * self.scale)

    def scale_font(self, base_size):
        """Масштабирует размер шрифта с округлением до целого"""
        size = int(base_size * self.scale)
        return max(8, min(size, base_size * 2))  # Ограничиваем снизу и сверху

    def on_title_double_click(self, event):
        """Обрабатывает двойной клик по заголовку окна"""
        # Проверяем, что клик был по заголовку (приблизительно)
        if event.y < 30:  # Высота заголовка обычно 20-30px
            self.toggle_window_size()

    def toggle_window_size(self):
        """Переключает между полноэкранным режимом и 1280x720"""
        if self.is_fullscreen:
            self.root.state('normal')
            self.root.geometry("1280x720")
            
            # Центрируем
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - 1280) // 2
            y = (screen_height - 720) // 2
            self.root.geometry(f"+{x}+{y}")
            
            self.is_fullscreen = False
        else:
            self.root.state('zoomed')
            self.is_fullscreen = True
        
        # ✅ ОБНОВЛЯЕМ МЕНЮ ПОСЛЕ ПЕРЕКЛЮЧЕНИЯ
        if not hasattr(self, 'game_started') or not self.game_started:
            self.root.after(200, self.create_start_menu)

    def on_window_resize(self, event):
        """Обрабатывает изменение размера окна"""
        if event.widget != self.root:
            return
        
        if self.root.state() == 'iconic':
            return
        
        # Обновляем масштаб
        self.update_scale()
        
        # Если игра запущена - обновляем ячейки
        if hasattr(self, 'game_started') and self.game_started:
            if hasattr(self, '_resize_timer'):
                self.root.after_cancel(self._resize_timer)
            self._resize_timer = self.root.after(200, self.update_cell_sizes)
        
        # Если в меню - пересоздаём меню
        elif not hasattr(self, 'game_started') or not self.game_started:
            if hasattr(self, '_resize_timer'):
                self.root.after_cancel(self._resize_timer)
            self._resize_timer = self.root.after(300, self._force_recreate_menu)

    def _force_recreate_menu(self):
        """Принудительно пересоздаёт меню с новым масштабом"""
        if not hasattr(self, 'game_started') or not self.game_started:
            self.create_start_menu()
            self._resize_timer = None

    def update_scale(self):
        """Обновляет коэффициент масштабирования на основе текущего размера окна"""
        try:
            self.root.update_idletasks()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # Если окно свернуто или имеет нулевой размер - пропускаем
            if window_width < 100 or window_height < 100:
                return
            
            # Рассчитываем масштаб относительно базового размера
            scale_x = window_width / self.BASE_WIDTH
            scale_y = window_height / self.BASE_HEIGHT
            self.current_scale = min(scale_x, scale_y)
            
            # Ограничиваем масштаб
            if self.current_scale > 1.8:
                self.current_scale = 1.8
            elif self.current_scale < 0.35:
                self.current_scale = 0.35
            
            # Сохраняем для обратной совместимости
            self.scale = self.current_scale
            self.scale_x = scale_x
            self.scale_y = scale_y
            
            # Обновляем категорию экрана
            self.screen_category = self.get_screen_category()
            
            print(f"🔄 Обновлён масштаб: {self.current_scale:.2f} (окно: {window_width}x{window_height})")
            
            return self.current_scale
        except:
            return self.current_scale

    def update_scale_for_current_size(self):
        """Обновляет коэффициенты масштабирования для текущего размера окна"""
        # Получаем текущий размер окна
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Рассчитываем масштаб относительно базового размера
        self.scale_x = window_width / self.BASE_WIDTH
        self.scale_y = window_height / self.BASE_HEIGHT
        self.scale = min(self.scale_x, self.scale_y)
        
        # Ограничиваем масштаб
        self.scale = max(0.6, min(1.5, self.scale))
        
        # Обновляем категорию экрана
        self.screen_category = self.get_screen_category()
        
        print(f"🔄 Обновлён масштаб: {self.scale:.2f} (окно: {window_width}x{window_height})")

    def on_root_close(self):
        """Обработка закрытия главного окна"""
        # Закрываем все побочные окна
        self.close_all_windows()
        # Закрываем игру
        self.root.quit()

    def load_window_icon(self):
        try:
            from PIL import Image, ImageTk
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                # ТОЧНО КАК В ТЕСТЕ
                self.root.iconbitmap(icon_path)
                
                img = Image.open(icon_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                icon = ImageTk.PhotoImage(img)
                
                # СОХРАНЯЕМ В root (КАК В ТЕСТЕ)
                self.root._icon = icon
                
                self.root.iconphoto(True, icon)
                self.root.iconphoto(False, icon)
                print(f"✅ Иконка загружена")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def create_styled_dialog(self, title, content_func, width_min=400, width_max=800, height_min=300, height_max=600):
        """
        Создаёт стилизованное диалоговое окно с автоматической подгонкой размера
        """
        dialog = tk.Toplevel(self.root)
        dialog.resizable(False, False)
        dialog.title(title)
        dialog.configure(bg='#2a3a2a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = tk.Frame(dialog, bg='#2a3a2a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        content_func(main_frame)
        
        self.apply_hover_effect_to_all_buttons(dialog)
        
        # ✅ ДВАЖДЫ ОБНОВЛЯЕМ ДЛЯ ТОЧНОГО РАСЧЁТА
        dialog.update_idletasks()
        dialog.update()
        
        # ✅ ПРИНУДИТЕЛЬНО ВЫЧИСЛЯЕМ РАЗМЕР
        req_width = main_frame.winfo_reqwidth() + 40
        req_height = main_frame.winfo_reqheight() + 40
        
        # Если ширина меньше минимальной - устанавливаем минимальную
        width = max(width_min, min(width_max, req_width))
        height = max(height_min, min(height_max, req_height))
        
        # ✅ Если это правила - делаем окно шире
        if "ПРАВИЛА" in title.upper():
            width = max(width, 700)  # Минимальная ширина для правил
        
        dialog.geometry(f"{width}x{height}")
        
        # Центрируем
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        return dialog

    def init_horse_owners(self):
        """Создаёт фермеров-владельцев лошадей с разным уровнем богатства"""
        self.horse_owners = {}
        
        for name in OWNER_NAMES:
            self.horse_owners[name] = HorseOwner(
                name=name,
                color=OWNER_COLORS.get(name, "#888888"),
                wealth=OWNER_WEALTH.get(name, 2)
            )

    def distribute_initial_horses(self):
        """Распределяет всех лошадей между фермерами в начале игры"""
        # 10 лошадей 1 уровня, 8 лошадей 2 уровня, 4 лошади 3 уровня
        horse_distribution = {
            1: 10,
            2: 8,
            3: 4
        }
        
        all_horses = []
        for level, count in horse_distribution.items():
            for _ in range(count):
                horse = self.create_horse(level, False)
                all_horses.append(horse)
        
        # Перемешиваем
        random.shuffle(all_horses)
        
        # Получаем список владельцев
        owners = list(self.horse_owners.values())
        
        # Распределяем лошадей равномерно между всеми владельцами
        # Сначала вычисляем базовое количество лошадей на владельца
        base_count = len(all_horses) // len(owners)
        remainder = len(all_horses) % len(owners)
        
        distribution = []
        for i, owner in enumerate(owners):
            count = base_count + (1 if i < remainder else 0)
            distribution.append((owner, count))
        
        idx = 0
        for owner, count in distribution:
            for _ in range(count):
                if idx < len(all_horses):
                    horse = all_horses[idx]
                    horse.owner_color = owner.color
                    owner.horses.append(horse)
                    idx += 1

    def init_market_horses(self):
        """Выставляет 4 случайных лошади на продажу от разных фермеров"""
        # ✅ ОЧИЩАЕМ СПИСКИ ПРОДАЖИ
        for owner in self.horse_owners.values():
            owner.horses_for_sale = []
        
        # Собираем всех лошадей от фермеров
        all_farmer_horses = []
        for owner in self.horse_owners.values():
            for horse in owner.horses:
                all_farmer_horses.append((owner, horse))
        
        # Перемешиваем
        random.shuffle(all_farmer_horses)
        
        # Выставляем до 4 лошадей
        sold_count = 0
        used_owners = set()
        
        for owner, horse in all_farmer_horses:
            if sold_count >= 4:
                break
            if owner.name not in used_owners or len(used_owners) >= 4:
                owner.horses_for_sale.append(horse)
                used_owners.add(owner.name)
                sold_count += 1
        
        # Если не набрали 4, добираем оставшимися
        if sold_count < 4:
            for owner, horse in all_farmer_horses:
                if sold_count >= 4:
                    break
                if horse not in owner.horses_for_sale:
                    owner.horses_for_sale.append(horse)
                    sold_count += 1


    def get_unique_horse_name(self):
        """Возвращает уникальное имя лошади"""
        # Смешиваем все имена
        all_names = HORSE_NAMES
        available_names = [name for name in all_names if name not in self.used_horse_names]
        
        if not available_names:
            # Комбинируем имена
            for n1 in ["Быстрый", "Гордый", "Вольный", "Смелый", "Сильный"]:
                for n2 in HORSE_NAMES[:10]:
                    new_name = f"{n1} {n2}"
                    if new_name not in self.used_horse_names:
                        self.used_horse_names.add(new_name)
                        return new_name
            counter = len(self.used_horse_names) + 1
            return f"Скакун {counter}"
        
        name = random.choice(available_names)
        self.used_horse_names.add(name)
        return name

    def create_horse(self, level, is_temp=False):
        """Создаёт лошадь с уникальным именем"""
        name = self.get_unique_horse_name()
        return Horse(level, name, "#FFD700", is_temp)

    def load_horse_images(self):
        images_dir = Path(resource_path("horse_images"))
        images_dir.mkdir(exist_ok=True)
        
        for level in [1, 2, 3]:
            img_path = images_dir / f"horse_{level}.png"
            if img_path.exists():
                try:
                    img = Image.open(img_path).resize((80, 80), Image.Resampling.LANCZOS)
                    self.horse_images[level] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Ошибка загрузки {img_path}: {e}")
                    self.horse_images[level] = None
            else:
                print(f"Файл не найден: {img_path}")
                self.horse_images[level] = None
    
    def apply_hover_to_all_widgets(self, widget):
        """Рекурсивно применяет эффект наведения ко всем виджетам"""
        if isinstance(widget, tk.Button):
            original_bg = widget.cget('bg')
            if original_bg == '#4a7a2e':
                hover_color = '#5a9a3e'
            elif original_bg == '#8B4513':
                hover_color = '#a06030'
            elif original_bg == '#6E3E2E':
                hover_color = '#8e5a4e'
            elif original_bg == '#555555':
                hover_color = '#777777'
            else:
                hover_color = original_bg
            
            def on_enter(e, btn=widget, color=hover_color):
                btn.config(bg=color, cursor="hand2")
            
            def on_leave(e, btn=widget, color=original_bg):
                btn.config(bg=color)
            
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.config(cursor="hand2")
        
        for child in widget.winfo_children():
            self.apply_hover_to_all_widgets(child)

    def show_end_game_overlay(self):
        """Показывает финальный оверлей с рейтингом игроков"""
        
        # Проверяем, не существует ли уже оверлей
        if hasattr(self, 'end_game_overlay') and self.end_game_overlay and self.end_game_overlay.winfo_exists():
            return
        
        # Создаём затемнённый фон
        overlay = tk.Toplevel(self.root)
        overlay.overrideredirect(True)
        overlay.configure(bg='#000000')
        overlay.attributes('-alpha', 0.95)
        
        # Связываем с главным окном
        overlay.transient(self.root)
        
        # Блокируем закрытие через крестик
        overlay.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Сохраняем ссылку на оверлей
        self.end_game_overlay = overlay
        
        # Растягиваем на всё окно
        overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")
        
        # Основной контейнер
        main_frame = tk.Frame(overlay, bg='#2a3a2a', relief='ridge', bd=5)
        main_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Заголовок
        tk.Label(main_frame, text="🏆 ИГРА ОКОНЧЕНА 🏆", 
                font=('Arial', 32, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=30)
        
        # ✅ ПОКАЗЫВАЕМ ВСЕХ ИГРОКОВ (включая банкротов)
        # Сортируем по капиталу (банкроты будут с капиталом 0)
        all_players = sorted(self.players, key=lambda p: p.total_capital if not p.is_bankrupt else -1, reverse=True)
        
        # Проверяем рекорд (только среди небанкротов)
        active_players = [p for p in self.players if not p.is_bankrupt]
        winner = active_players[0] if active_players else None
        is_record = self.records.check_and_update_record(winner) if winner else False
        
        # Таблица рейтинга
        table_frame = tk.Frame(main_frame, bg='#1a2a1a', relief='sunken', bd=3)
        table_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Заголовки таблицы
        headers = ["Место", "Игрок", "Капитал", "Лошадей", "Построек", "Статус"]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=('Arial', 14, 'bold'),
                    bg='#1a2a1a', fg='#FFD700', padx=20, pady=10).grid(row=0, column=col, sticky='nsew')
        
        # Заполнение таблицы
        place = 0
        for i, player in enumerate(all_players):
            if player.is_bankrupt:
                # Банкроты - показываем в конце списка
                row = i + 1
                medal = "💀"
                capital = player.total_capital
                capital_gold = capital // QUARTERS_PER_GOLD
                capital_q = capital % QUARTERS_PER_GOLD
                
                horses_count = len([h for h in player.horses if not h.is_temp])
                buildings = player.stables + player.fields
                
                capital_str = f"{capital_gold}.{capital_q} зол." if capital_q > 0 else f"{capital_gold} зол."
                
                tk.Label(table_frame, text=medal, font=('Arial', 12),
                        bg='#1a2a1a', fg='#FF4444', padx=20, pady=5).grid(row=row, column=0, sticky='nsew')
                tk.Label(table_frame, text=player.name, font=('Arial', 12),
                        bg='#1a2a1a', fg='#FF4444', padx=20, pady=5).grid(row=row, column=1, sticky='nsew')
                tk.Label(table_frame, text=capital_str, font=('Arial', 12),
                        bg='#1a2a1a', fg='#FF4444', padx=20, pady=5).grid(row=row, column=2, sticky='nsew')
                tk.Label(table_frame, text=str(horses_count), font=('Arial', 12),
                        bg='#1a2a1a', fg='#FF4444', padx=20, pady=5).grid(row=row, column=3, sticky='nsew')
                tk.Label(table_frame, text=str(buildings), font=('Arial', 12),
                        bg='#1a2a1a', fg='#FF4444', padx=20, pady=5).grid(row=row, column=4, sticky='nsew')
                tk.Label(table_frame, text="💀 БАНКРОТ", font=('Arial', 12, 'bold'),
                        bg='#1a2a1a', fg='#FF4444', padx=20, pady=5).grid(row=row, column=5, sticky='nsew')
            else:
                place += 1
                row = place
                medal = "🥇" if place == 1 else "🥈" if place == 2 else "🥉" if place == 3 else f"{place}."
                capital = player.total_capital
                capital_gold = capital // QUARTERS_PER_GOLD
                capital_q = capital % QUARTERS_PER_GOLD
                
                horses_count = len([h for h in player.horses if not h.is_temp])
                buildings = player.stables + player.fields
                
                capital_str = f"{capital_gold}.{capital_q} зол." if capital_q > 0 else f"{capital_gold} зол."
                
                tk.Label(table_frame, text=medal, font=('Arial', 12),
                        bg='#1a2a1a', fg='#FFD700' if place == 1 else 'white', padx=20, pady=5).grid(row=row, column=0, sticky='nsew')
                tk.Label(table_frame, text=player.name, font=('Arial', 12),
                        bg='#1a2a1a', fg='#FFD700' if place == 1 else 'white', padx=20, pady=5).grid(row=row, column=1, sticky='nsew')
                tk.Label(table_frame, text=capital_str, font=('Arial', 12),
                        bg='#1a2a1a', fg='#FFD700' if place == 1 else '#90EE90', padx=20, pady=5).grid(row=row, column=2, sticky='nsew')
                tk.Label(table_frame, text=str(horses_count), font=('Arial', 12),
                        bg='#1a2a1a', fg='white', padx=20, pady=5).grid(row=row, column=3, sticky='nsew')
                tk.Label(table_frame, text=str(buildings), font=('Arial', 12),
                        bg='#1a2a1a', fg='white', padx=20, pady=5).grid(row=row, column=4, sticky='nsew')
                tk.Label(table_frame, text="✅ В ИГРЕ", font=('Arial', 12, 'bold'),
                        bg='#1a2a1a', fg='#90EE90', padx=20, pady=5).grid(row=row, column=5, sticky='nsew')
        
        # Настройка растягивания колонок
        for col in range(len(headers)):
            table_frame.grid_columnconfigure(col, weight=1)
        
        # Информация о рекорде
        record_frame = tk.Frame(main_frame, bg='#2a3a2a')
        record_frame.pack(pady=20)
        
        if is_record and winner:
            record_text = f"🏆 НОВЫЙ РЕКОРД! 🏆\n{winner.name} побил рекорд!"
            record_color = '#FFD700'
        elif self.records.record_holder:
            record_text = f"📜 РЕКОРД ИГРЫ: {self.records.record_holder}\nКапитал: {self.records.record_capital//QUARTERS_PER_GOLD}.{self.records.record_capital%QUARTERS_PER_GOLD} зол."
            record_color = '#C0C0C0'
        else:
            record_text = "Рекордов пока нет"
            record_color = '#888888'
        
        tk.Label(record_frame, text=record_text, font=('Arial', 14, 'bold'),
                bg='#2a3a2a', fg=record_color, justify='center').pack()
        
        # Кнопки
        btn_frame = tk.Frame(main_frame, bg='#2a3a2a')
        btn_frame.pack(pady=30)
        
        def on_new_game():
            overlay.destroy()
            self.restart_from_overlay()
        
        def on_exit():
            overlay.destroy()
            self.exit_from_overlay()
        
        new_game_btn = tk.Button(btn_frame, text="🎮 НОВАЯ ИГРА", 
                                command=on_new_game,
                                bg='#4a7a2e', fg='white', font=('Arial', 16, 'bold'),
                                padx=40, pady=10, cursor="hand2")
        new_game_btn.pack(side='left', padx=15)
        
        exit_btn = tk.Button(btn_frame, text="🚪 ВЫХОД", 
                            command=on_exit,
                            bg='#8B4513', fg='white', font=('Arial', 16, 'bold'),
                            padx=40, pady=10, cursor="hand2")
        exit_btn.pack(side='left', padx=15)
        
        # Эффекты наведения для кнопок
        def on_enter(btn, color):
            btn.config(bg=color)
        
        def on_leave(btn, color):
            btn.config(bg=color)
        
        new_game_btn.bind("<Enter>", lambda e: on_enter(new_game_btn, '#5a9a3e'))
        new_game_btn.bind("<Leave>", lambda e: on_leave(new_game_btn, '#4a7a2e'))
        exit_btn.bind("<Enter>", lambda e: on_enter(exit_btn, '#a06030'))
        exit_btn.bind("<Leave>", lambda e: on_leave(exit_btn, '#8B4513'))
        
        # Применяем эффект наведения ко всем кнопкам
        self.apply_hover_effect_to_all_buttons(main_frame)
        
        # Останавливаем игру
        self.game_active = False
        self.sound.stop_music()
        self.sound.play('win')

        
        # Показываем оверлей поверх всего
        overlay.lift()
        overlay.focus_force()
        
        # Ждём, пока оверлей не будет закрыт
        overlay.wait_window()

    def exit_from_overlay(self):
        """Выход из игры из финального оверлея"""
        if hasattr(self, 'end_game_overlay'):
            self.end_game_overlay = None
        
        self.sound.stop_music()
        # ✅ Только quit, без destroy
        self.root.quit()

    def restart_from_overlay(self):
        """Перезапускает игру из финального оверлея"""
        if hasattr(self, 'end_game_overlay'):
            self.end_game_overlay = None
        
        # Останавливаем музыку
        self.sound.stop_music()
        
        # ✅ Закрываем все дочерние окна
        for widget in self.root.winfo_children():
            try:
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
            except:
                pass
        
        # Очищаем корневое окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Сбрасываем состояние игры и создаём меню
        self.players = []
        self.current_player_idx = 0
        self.current_day = 1
        self.week_number = 1
        self.race_mode = False
        self.auction_mode = False
        self.race_participants = []
        self.available_tasks = []
        self.tasks_generated = False
        self.last_race_horse = {}
        self.event_overlay = None
        self.game_active = True
        self.warning_shown_today = False
        
        self.create_start_menu()

    def exit_to_menu(self, overlay):
        """Выход в главное меню из финального оверлея"""
        overlay.destroy()
        self.root.quit()
        self.__init__(self.root)

    def generate_auction_tasks(self):
        """Генерирует задания для текущего аукциона (лошади берутся от реальных владельцев)"""
        self.available_tasks = []
        
        # Собираем всех лошадей, которые есть у фермеров
        available_horses = []
        for owner in self.horse_owners.values():
            for horse in owner.horses:
                # БАЗОВАЯ ПРОВЕРКА: лошадь не достигла максимума прокачек
                total_upgrades = len(horse.upgrades) + horse.pending_upgrades
                if total_upgrades >= TRAINING_UPGRADES_MAX:
                    continue  # Пропускаем, если достигнут максимум
                
                # ✅ ПРОВЕРЯЕМ, УЧАСТВОВАЛА ЛИ ЛОШАДЬ В СКАЧКАХ НА ПРОШЛОЙ НЕДЕЛЕ
                # last_race_horse хранит {владелец: имя_лошади} для последних скачек
                # Если лошадь участвовала в прошлых скачках - пропускаем её для задания "win_race"
                available_horses.append((owner, horse))
        
        # Если лошадей меньше 4, берём и тех, что на продаже (но тоже с проверкой)
        if len(available_horses) < 4:
            for owner in self.horse_owners.values():
                for horse in owner.horses_for_sale:
                    if (owner, horse) not in available_horses:
                        total_upgrades = len(horse.upgrades) + horse.pending_upgrades
                        if total_upgrades < TRAINING_UPGRADES_MAX:
                            available_horses.append((owner, horse))
        
        # Перемешиваем
        random.shuffle(available_horses)
        
        # Берём до 4 лошадей для заданий
        selected = available_horses[:4]
        
        # Если меньше 4 лошадей доступно - дополняем случайными (если есть)
        if len(selected) < 4:
            # Пытаемся найти ещё лошадей
            all_remaining = []
            for owner in self.horse_owners.values():
                for horse in owner.horses:
                    if (owner, horse) not in selected:
                        total_upgrades = len(horse.upgrades) + horse.pending_upgrades
                        if total_upgrades < TRAINING_UPGRADES_MAX:
                            all_remaining.append((owner, horse))
            
            random.shuffle(all_remaining)
            needed = 4 - len(selected)
            selected.extend(all_remaining[:needed])
        
        for owner, original_horse in selected:
            # Дополнительная проверка для безопасности
            total_upgrades = len(original_horse.upgrades) + original_horse.pending_upgrades
            if total_upgrades >= TRAINING_UPGRADES_MAX:
                continue
            
            # ✅ ДЛЯ ЗАДАНИЯ "win_race" ПРОВЕРЯЕМ, НЕ УЧАСТВОВАЛА ЛИ ЛОШАДЬ В ПРОШЛЫХ СКАЧКАХ
            # Проверяем, есть ли эта лошадь в last_race_horse у её владельца
            horse_was_in_race = False
            if owner.name in self.last_race_horse:
                if self.last_race_horse[owner.name] == original_horse.name:
                    horse_was_in_race = True
            
            # Создаём ВРЕМЕННУЮ КОПИЮ для игрока
            temp_horse = Horse(original_horse.level, original_horse.name, owner.color, True)
            temp_horse.upgrades = original_horse.upgrades.copy()
            temp_horse.upgrade_count = len(temp_horse.upgrades)
            temp_horse.training_progress = original_horse.training_progress
            temp_horse.pending_upgrades = original_horse.pending_upgrades
            
            weekly_cost = (original_horse.food_per_day + original_horse.water_per_day) * 7
            base_advance = max(2 * QUARTERS_PER_GOLD, weekly_cost + 2)
            level = original_horse.level
            level_data = HORSE_LEVELS.get(level, HORSE_LEVELS[1])
            
            # ✅ Берем награды из структуры
            reward_care = level_data['rewards']['care']
            reward_train = level_data['rewards']['train']  # за прокачку
            reward_win = level_data['rewards']['win_race']
            
            weekly_cost = (original_horse.food_per_day + original_horse.water_per_day) * 7
            base_advance = max(2 * QUARTERS_PER_GOLD, weekly_cost + 2)
            
            # ✅ ВЫБИРАЕМ ТИП ЗАДАНИЯ С УЧЁТОМ ОГРАНИЧЕНИЙ
            # Доступные типы заданий
            available_task_types = ["care", "train"]
            
            # ✅ ДЛЯ "win_race" - только если лошадь НЕ участвовала в прошлых скачках
            if not horse_was_in_race:
                available_task_types.append("win_race")
            
            # Случайный выбор из доступных
            task_type = random.choice(available_task_types)
            
            if task_type == "care":
                reward_on_complete = reward_care
            elif task_type == "train":
                reward_on_complete = 0  # Не используется, награда вычисляется по уровню
            else:  # win_race
                reward_on_complete = reward_win
            
            # ✅ СОХРАНЯЕМ НАЧАЛЬНОЕ ОБЩЕЕ КОЛИЧЕСТВО ПРОКАЧЕК
            start_total_upgrades = len(original_horse.upgrades) + original_horse.pending_upgrades

            self.available_tasks.append({
                'horse': temp_horse,
                'original_horse': original_horse,
                'owner': owner,
                'task_type': task_type,
                'advance': base_advance,
                'reward': reward_on_complete,
                'weekly_cost': weekly_cost,
                'owner_name': owner.name,
                'taken': False,
                'start_total_upgrades': start_total_upgrades,
                'horse_was_in_race': horse_was_in_race  # ✅ Сохраняем для информации
            })
        
        self.tasks_generated = True

    def reload_ui(self):
        """Перезагружает интерфейс с новым масштабом"""
        # Проверяем, запущена ли игра
        if not hasattr(self, 'game_started') or not self.game_started:
            return
        
        # Сохраняем состояние
        current_race_mode = self.race_mode if hasattr(self, 'race_mode') else False
        current_auction_mode = self.auction_mode if hasattr(self, 'auction_mode') else False
        current_race_participants = self.race_participants.copy() if hasattr(self, 'race_participants') and self.race_participants else []
        
        # Пересоздаём UI
        self.create_ui()
        
        # Восстанавливаем состояние
        self.race_mode = current_race_mode
        self.auction_mode = current_auction_mode
        self.race_participants = current_race_participants
        
        # Обновляем отображение
        self.update_actions_buttons()
        self.update_display()

    def load_horse_gif(self):
        """Загружает GIF для анимации тренировки из папки gif"""
        gif_dir = Path(resource_path("gif"))
        gif_dir.mkdir(exist_ok=True)
        
        gif_path = gif_dir / "horse.gif"
        self.horse_gif_frames = []
        
        if gif_path.exists():
            try:
                gif = Image.open(gif_path)
                for frame in ImageSequence.Iterator(gif):
                    frame_copy = frame.copy().resize((150, 150), Image.Resampling.LANCZOS)
                    self.horse_gif_frames.append(ImageTk.PhotoImage(frame_copy))
            except Exception as e:
                print(f"Ошибка загрузки horse.gif: {e}")
    
    def create_styled_button(self, parent, text, command, color, hover_color=None, cursor="hand2"):
        """Создаёт кнопку с подсветкой при наведении"""
        if hover_color is None:
            # Затемняем цвет для подсветки
            if color == '#4a7a2e':
                hover_color = '#5a9a3e'
            elif color == '#8B4513':
                hover_color = '#a06030'
            elif color == '#6E3E2E':
                hover_color = '#8e5a4e'
            else:
                hover_color = color
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg='white', font=('Arial', 13, 'bold'), 
                       padx=40, pady=10, relief='raised', width=22,
                       cursor=cursor, activebackground=hover_color, activeforeground='white')
        
        # Эффект при наведении
        def on_enter(e):
            btn.config(bg=hover_color)
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def apply_hover_effect_to_all_buttons(self, parent):
        """Рекурсивно применяет эффект подсветки и звук наведения ко всем кнопкам"""
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Button):
                # Сохраняем оригинальный цвет
                original_bg = widget.cget('bg')
                # Находим цвет подсветки
                if original_bg == '#4a7a2e':
                    hover_color = '#5a9a3e'
                elif original_bg == '#8B4513':
                    hover_color = '#a06030'
                elif original_bg == '#6E3E2E':
                    hover_color = '#8e5a4e'
                elif original_bg == '#555555':
                    hover_color = '#777777'
                else:
                    hover_color = original_bg
                
                # Флаг для предотвращения многократного воспроизведения
                hover_played = False
                
                def on_enter(e, btn=widget, color=hover_color):
                    nonlocal hover_played
                    btn.config(bg=color, cursor="hand2")
                    # Воспроизводим звук только один раз при входе
                    if not hover_played:
                        self.sound.play_hover()
                        hover_played = True
                
                def on_leave(e, btn=widget, color=original_bg):
                    nonlocal hover_played
                    btn.config(bg=color)
                    hover_played = False  # Сбрасываем флаг для следующего наведения
                
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.config(cursor="hand2")
            else:
                self.apply_hover_effect_to_all_buttons(widget)

    def create_start_menu(self):
        # Очищаем всё
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg='#1a2a1a')
        self.root.config(cursor="crosshair")
        
        # ✅ ОБНОВЛЯЕМ МАСШТАБ
        self.update_scale()
        scale = self.current_scale
        
        # Получаем размер окна
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        print(f"🔄 СОЗДАНИЕ МЕНЮ: {window_width}x{window_height}, масштаб: {scale:.2f}")
        
        # ✅ ОПРЕДЕЛЯЕМ КАТЕГОРИЮ ПО ВЫСОТЕ
        is_small_height = window_height < 800
        is_very_small_height = window_height < 650
        
        # ✅ РАЗМЕРЫ В ЗАВИСИМОСТИ ОТ ВЫСОТЫ ОКНА
        if is_very_small_height:
            # Очень маленькое окно - минимальные размеры
            title_size = 18
            subtitle_size = 12
            button_size = 11
            small_text_size = 9
            version_size = 8
            padding = 8
            button_padx = 15
            button_pady = 6
            button_width = 18
            border_width = 2
            button_spacing = 3
            show_record = False
            show_version = True
        elif is_small_height:
            # Маленькое окно - уменьшенные размеры
            title_size = 22
            subtitle_size = 14
            button_size = 13
            small_text_size = 10
            version_size = 9
            padding = 12
            button_padx = 25
            button_pady = 8
            button_width = 20
            border_width = 3
            button_spacing = 4
            show_record = True
            show_version = True
        else:
            # Нормальное окно - стандартные размеры
            title_size = max(24, int(34 * scale))
            subtitle_size = max(14, int(18 * scale))
            button_size = max(12, int(18 * scale))
            small_text_size = max(10, int(14 * scale))
            version_size = max(8, int(11 * scale))
            padding = max(15, int(20 * scale))
            button_padx = max(20, int(50 * scale))
            button_pady = max(8, int(14 * scale))
            button_width = max(20, int(26 * scale))
            border_width = max(2, int(5 * scale))
            button_spacing = int(6 * scale)
            show_record = True
            show_version = True
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#1a2a1a')
        main_frame.pack(fill='both', expand=True)
        
        # ✅ ПРИ МАЛЕНЬКОЙ ВЫСОТЕ - МЕНЯЕМ ПРОПОРЦИИ
        if is_very_small_height:
            # GIF занимает меньше места, больше места для меню
            left_percent = 0.35
        elif is_small_height:
            left_percent = 0.40
        else:
            left_percent = 0.45
        
        # ЛЕВАЯ КОЛОНКА - GIF
        left_frame = tk.Frame(main_frame, bg='#1a2a1a')
        left_frame.pack(side='left', fill='both', expand=True, padx=padding, pady=padding)
        
        # ПРАВАЯ КОЛОНКА - МЕНЮ
        right_frame = tk.Frame(main_frame, bg='#1a2a1a')
        right_frame.pack(side='right', fill='both', expand=True, padx=padding, pady=padding)
        
        # === ЛЕВАЯ ЧАСТЬ - АНИМАЦИЯ ===
        animation_container = tk.Frame(left_frame, bg='#2a3a2a', relief='ridge', bd=border_width)
        animation_container.pack(fill='both', expand=True)
        
        # ✅ ЗАГРУЖАЕМ GIF С УЧЁТОМ ВЫСОТЫ
        self.load_splash_gif_with_size(window_width, window_height, is_very_small_height)
        
        if hasattr(self, 'splash_frames') and self.splash_frames:
            self.splash_label = tk.Label(animation_container, bg='#2a3a2a', cursor="heart")
            self.splash_label.pack(expand=True, fill='both')
            self.current_splash_frame = 0
            self.animate_splash_optimized()
        else:
            # Запасной вариант без GIF
            tk.Label(animation_container, text="🐎 ЛОШАДИ И РЕДИСКИ 🥕", 
                    font=('Arial', title_size, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(expand=True, pady=10)
            tk.Label(animation_container, text="Фермерская стратегия", 
                    font=('Arial', subtitle_size), bg='#2a3a2a', fg='white').pack(pady=5)
        
        # === ПРАВАЯ ЧАСТЬ - КНОПКИ МЕНЮ ===
        right_container = tk.Frame(right_frame, bg='#2a3a2a', relief='ridge', bd=border_width)
        right_container.pack(fill='both', expand=True)
        
        # Центрируем содержимое
        content_frame = tk.Frame(right_container, bg='#2a3a2a')
        content_frame.pack(expand=True, padx=padding, pady=padding)
        
        # ✅ ЗАГОЛОВОК - СКРЫВАЕМ ПРИ ОЧЕНЬ МАЛЕНЬКОЙ ВЫСОТЕ
        if not is_very_small_height:
            tk.Label(content_frame, text="🐎 ЛОШАДИ И РЕДИСКИ 🥕", 
                    font=('Arial', title_size, 'bold'), bg='#2a3a2a', fg='#FFD700', cursor="trek").pack(pady=(0, 3))
        
        tk.Label(content_frame, text="Фермерская стратегия", 
                font=('Arial', subtitle_size), bg='#2a3a2a', fg='white', cursor="trek").pack(pady=(0, 8 if not is_very_small_height else 3))
        
        # ✅ РЕКОРД - СКРЫВАЕМ ПРИ МАЛЕНЬКОЙ ВЫСОТЕ
        if show_record and self.records.record_holder:
            record_frame = tk.Frame(content_frame, bg='#2a3a2a')
            record_frame.pack(pady=(0, 8))
            
            tk.Label(record_frame, text=f"🏆 {self.records.record_holder}", 
                    font=('Arial', small_text_size, 'bold'), bg='#2a3a2a', fg='#FFD700').pack()
            if not is_small_height:
                tk.Label(record_frame, text=f"Капитал: {self.records.record_capital//QUARTERS_PER_GOLD}.{self.records.record_capital%QUARTERS_PER_GOLD} зол.", 
                        font=('Arial', small_text_size - 1), bg='#2a3a2a', fg='#90EE90').pack()
        
        # Разделитель (показываем только если есть место)
        if not is_very_small_height:
            tk.Frame(content_frame, bg='#4a7a2e', height=2).pack(fill='x', padx=20, pady=5)
        
        # КНОПКИ
        buttons_frame = tk.Frame(content_frame, bg='#2a3a2a')
        buttons_frame.pack(pady=int(8 * scale if scale < 1 else 15 * scale), expand=True)
        
        # ✅ СПИСОК КНОПОК - УКОРОЧЕННЫЙ ПРИ МАЛЕНЬКОЙ ВЫСОТЕ
        if is_very_small_height:
            menu_buttons = [
                ("▶ НАЧАТЬ", self.start_game, '#4a7a2e'),
                ("📂 ЗАГРУЗИТЬ", self.show_load_dialog, '#4a7a2e'),
                ("📖 ПРАВИЛА", self.show_rules, '#6E3E2E'),
                ("ℹ️ ОБ ИГРЕ", self.show_about, '#6E3E2E'),
                ("🔊 ЗВУК", self.open_sound_settings, '#4a7a2e'),
                ("✕ ВЫХОД", self.exit_game, '#8B4513')
            ]
        elif is_small_height:
            menu_buttons = [
                ("🎮 НАЧАТЬ ИГРУ", self.start_game, '#4a7a2e'),
                ("📂 ЗАГРУЗИТЬ ИГРУ", self.show_load_dialog, '#4a7a2e'),
                ("📖 ПРАВИЛА", self.show_rules, '#6E3E2E'),
                ("ℹ️ ОБ ИГРЕ", self.show_about, '#6E3E2E'),
                ("🔊 НАСТРОЙКИ ЗВУКА", self.open_sound_settings, '#4a7a2e'),
                ("🚪 ВЫХОД", self.exit_game, '#8B4513')
            ]
        else:
            menu_buttons = [
                ("🎮 НАЧАТЬ ИГРУ", self.start_game, '#4a7a2e'),
                ("📂 ЗАГРУЗИТЬ ИГРУ", self.show_load_dialog, '#4a7a2e'),
                ("📖 ПРАВИЛА", self.show_rules, '#6E3E2E'),
                ("ℹ️ ОБ ИГРЕ", self.show_about, '#6E3E2E'),
                ("🔊 НАСТРОЙКИ ЗВУКА", self.open_sound_settings, '#4a7a2e'),
                ("🚪 ВЫХОД", self.exit_game, '#8B4513')
            ]
        
        for text, cmd, color in menu_buttons:
            btn = tk.Button(buttons_frame, text=text, 
                           command=lambda c=cmd: self.menu_click(c),
                           bg=color, fg='white', 
                           font=('Arial', button_size, 'bold'),
                           padx=button_padx, pady=button_pady,
                           width=button_width, cursor="hand2")
            btn.pack(pady=button_spacing)
        
        self.apply_hover_effect_to_all_buttons(self.root)
        
        # ✅ ВЕРСИЯ - ВСЕГДА ПОКАЗЫВАЕМ (НО МАЛЕНЬКИМ ШРИФТОМ)
        if show_version:
            tk.Label(content_frame, text=get_version_string(), font=('Arial', version_size), 
                    bg='#2a3a2a', fg='gray', cursor="trek").pack(side='bottom', pady=5)

    def load_splash_gif_with_size(self, window_width, window_height, is_very_small=False):
        """Загружает GIF с размером под текущее окно"""
        gif_dir = Path(resource_path("gif"))
        gif_dir.mkdir(exist_ok=True)
        
        gif_path = gif_dir / "splash.gif"
        self.splash_frames = []
        
        if gif_path.exists():
            try:
                with Image.open(gif_path) as gif:
                    original_width, original_height = gif.size
                    
                    # ✅ УЧИТЫВАЕМ ВЫСОТУ ОКНА
                    if is_very_small:
                        # Очень маленькое окно - GIF занимает меньше места
                        available_height = int(window_height * 0.65) - 20
                        available_width = int(window_width * 0.32) - 20
                    else:
                        available_height = int(window_height * 0.80) - 30
                        available_width = int(window_width * 0.38) - 30
                    
                    # Минимальный размер
                    available_height = max(100, available_height)
                    available_width = max(100, available_width)
                    
                    # Рассчитываем размер с сохранением пропорций
                    scale_w = available_width / original_width
                    scale_h = available_height / original_height
                    scale = min(scale_w, scale_h)
                    
                    target_width = int(original_width * scale)
                    target_height = int(original_height * scale)
                    
                    # Минимальный размер для GIF
                    target_width = max(100, target_width)
                    target_height = max(130, target_height)
                    
                    print(f"📐 Загрузка GIF: {target_width}x{target_height}")
                    
                    for frame in ImageSequence.Iterator(gif):
                        frame_copy = frame.copy().resize((target_width, target_height), Image.Resampling.LANCZOS)
                        self.splash_frames.append(ImageTk.PhotoImage(frame_copy))
                        
            except Exception as e:
                print(f"Ошибка загрузки splash.gif: {e}")
                self.splash_frames = []
        
        return len(self.splash_frames) > 0

    def load_splash_gif(self):
        """Загружает GIF с размером под текущее окно (обёртка)"""
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        return self.load_splash_gif_with_size(window_width, window_height)

    def animate_splash_optimized(self):
        """Анимирует GIF с оптимальной скоростью"""
        try:
            if (hasattr(self, 'splash_label') and 
                self.splash_label and 
                self.splash_label.winfo_exists() and 
                self.splash_frames):
                
                self.current_splash_frame = (self.current_splash_frame + 1) % len(self.splash_frames)
                
                try:
                    self.splash_label.config(image=self.splash_frames[self.current_splash_frame])
                except tk.TclError:
                    pass
                
                # Скорость зависит от количества кадров
                delay = max(50, min(120, 1000 // len(self.splash_frames)))
                self.root.after(delay, self.animate_splash_optimized)
        except:
            pass

    def animate_splash_simple(self):
        """Простая анимация GIF без тормозов"""
        try:
            if (hasattr(self, 'splash_label') and 
                self.splash_label and 
                self.splash_label.winfo_exists() and 
                self.splash_frames):
                
                self.current_splash_frame = (self.current_splash_frame + 1) % len(self.splash_frames)
                self.splash_label.config(image=self.splash_frames[self.current_splash_frame])
                self.root.after(100, self.animate_splash_simple)
        except:
            pass  # Игнорируем ошибки при закрытии

    def on_menu_window_resize(self, event):
        """Обрабатывает изменение размера окна в меню"""
        if event.widget != self.root:
            return
        
        # Игнорируем, если окно свернуто
        if self.root.state() == 'iconic':
            return
        
        # Обновляем GIF с задержкой для плавности
        if hasattr(self, '_resize_timer'):
            self.root.after_cancel(self._resize_timer)
        
        self._resize_timer = self.root.after(300, self._delayed_menu_resize)

    def _delayed_menu_resize(self):
        """Отложенное обновление меню при изменении размера"""
        # Обновляем GIF
        self.update_splash_gif_size()
        
        # Обновляем масштаб
        self.update_scale_for_current_size()

    def animate_splash(self):
        """Анимация GIF на начальном экране"""
        try:
            if (hasattr(self, 'splash_label') and 
                self.splash_label and 
                self.splash_label.winfo_exists() and 
                self.splash_frames):
                
                self.current_splash_frame = (self.current_splash_frame + 1) % len(self.splash_frames)
                
                try:
                    self.splash_label.config(image=self.splash_frames[self.current_splash_frame])
                except tk.TclError:
                    # Если изображение не загрузилось, пропускаем кадр
                    pass
                
                # Скорость анимации зависит от количества кадров
                delay = max(50, min(150, 1000 // len(self.splash_frames)))
                self.root.after(delay, self.animate_splash)
        except (tk.TclError, AttributeError, RuntimeError):
            # Виджет был уничтожен - останавливаем анимацию
            pass
    
    def show_load_dialog(self):
        dialog = SaveLoadDialog(self.root, self.saves_dir, self.sound, is_load=True)
        self.root.wait_window(dialog)
        if dialog.result is not None:
            saves = list(self.saves_dir.glob("*.json"))
            saves.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            if dialog.result < len(saves):
                self.load_game_from_file(saves[dialog.result])
    
    def menu_click(self, cmd):
        self.sound.play('click')
        cmd()
    
    def start_game(self):
        self.setup_players()
        
        # ПРОВЕРКА: если игроки не были созданы (нажата ОТМЕНА)
        if not self.players:
            self.create_start_menu()  # Возвращаемся в меню
            return
        
        self.game_started = True
        self.warning_shown_today = False
        self._warning_shown_this_turn = False  # ✅ ДОБАВИТЬ
        self.create_ui()
        self.update_display()
        self.sound.play_music()
        self.sound.original_music_volume = self.sound.music_volume
    
    def create_upgrades_display(self, parent, horse, font_size=10, bg_color='#2a3a2a'):
        """
        Создаёт отображение прокачек лошади в виде цветных кружков ⚫
        
        Args:
            parent: родительский виджет (Frame)
            horse: объект лошади
            font_size: размер шрифта
            bg_color: цвет фона
        
        Returns:
            Frame с отображением прокачек
        """
        upgrade_frame = tk.Frame(parent, bg=bg_color)
        
        upgrade_display = horse.get_upgrade_display()
        for u in upgrade_display:
            if u == 'speed':
                color = '#FF6666'  # красный
            elif u == 'radish':
                color = '#90EE90'  # зелёный
            elif u == 'water':
                color = '#88AAFF'  # синий
            elif u == 'pending':
                color = '#FFFFFF'  # белый
            else:
                color = '#888888'  # серый
            
            tk.Label(upgrade_frame, text='⚫', font=('Arial', font_size), 
                    bg=bg_color, fg=color).pack(side='left')
        
        return upgrade_frame

    def get_upgrades_colored_text(self, horse):
        """
        Возвращает строку с цветными кружками ⚫ для вставки в Text виджет
        
        Args:
            horse: объект лошади
        
        Returns:
            Список кортежей (текст, тег) для вставки в Text виджет
        """
        result = []
        upgrade_display = horse.get_upgrade_display()
        for u in upgrade_display:
            if u == 'speed':
                result.append(('⚫', 'red'))
            elif u == 'radish':
                result.append(('⚫', 'green'))
            elif u == 'water':
                result.append(('⚫', 'blue'))
            elif u == 'pending':
                result.append(('⚫', 'white'))
            else:
                result.append(('⚫', 'gray'))
        return result

    def setup_players(self):
        dialog = StyledDialog(self.root, "Количество игроков", "Сколько людей играет?", 
                              ["1 игрок", "2 игрока", "3 игрока", "4 игрока"], 0, self.sound)
        self.root.wait_window(dialog)
        
        if dialog.result is None:
            self.players = []
            return
        
        num_humans = dialog.result + 1
        max_bots = 4 - num_humans
        
        if max_bots > 0:
            bot_dialog = NumericDialog(self.root, "Количество ботов", 
                                       f"Сколько ботов добавить? (макс {max_bots})", 
                                       max_bots, 0, self.sound)
            self.root.wait_window(bot_dialog)
            
            if bot_dialog.result is None:
                self.players = []
                return
            
            num_bots = bot_dialog.result
        else:
            num_bots = 0
        
        human_players = []
        bot_players = []
        
        for i in range(num_humans):
            name_dialog = NameDialog(self.root, "Имя игрока", f"Введите имя игрока {i+1}:", f"Фермер {i+1}", self.sound)
            self.root.wait_window(name_dialog)
            
            if name_dialog.result is None:
                self.players = []
                return
            
            name = name_dialog.result
            human_players.append(Player(name, PLAYER_COLORS[i % len(PLAYER_COLORS)], False, 0, self))
        
        # ✅ БОТАМ НАЗНАЧАЕМ СЛУЧАЙНЫЕ ИМЕНА ИЗ ГЛОБАЛЬНОГО СПИСКА
        shuffled_bot_names = BOT_NAMES.copy()
        random.shuffle(shuffled_bot_names)
        
        for i in range(num_bots):
            if i < len(shuffled_bot_names):
                name = shuffled_bot_names[i]
            else:
                name = f"AI_Бот_{i+1}"
            
            bot_players.append(Player(name, PLAYER_COLORS[(num_humans + i) % len(PLAYER_COLORS)], True, 0, self))
        
        all_players = human_players + bot_players
        random.shuffle(all_players)
        for order, player in enumerate(all_players):
            player.order = order + 1
        self.players = all_players
    
    def create_ui(self):
        # ✅ Сбрасываем флаги предупреждений
        self.warning_shown_today = False
        self._warning_shown_this_turn = False
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg='#1a2a1a')
        
        # === ВЕРХНЯЯ ПАНЕЛЬ (фиксированная) ===
        top_frame = tk.Frame(self.root, bg='#1a2a1a', height=90)
        top_frame.pack(fill='x', padx=10, pady=5)
        top_frame.pack_propagate(False)
        
        weekday = WEEKDAYS[(self.current_day - 1) % 7]
        event = WEEKDAY_EVENTS.get(weekday, "")
        
        self.info_label = tk.Label(top_frame, text="", font=('Arial', 14, 'bold'),
                                    bg='#1a2a1a', fg='#FFD700')
        self.info_label.pack(side='left', padx=20)
        
        self.weekday_label = tk.Label(top_frame, text=f"📅 {weekday} | {event}", font=('Arial', 12),
                                       bg='#1a2a1a', fg='#90EE90')
        self.weekday_label.pack(side='left', padx=20)
        
        self.resources_label = tk.Label(top_frame, text="", font=('Arial', 13),
                                        bg='#1a2a1a', fg='white')
        self.resources_label.pack(side='right', padx=20)
        
        menu_btn = tk.Button(top_frame, text="☰ МЕНЮ", command=self.open_menu, 
                            bg='#6E3E2E', fg='white', font=('Arial', 11, 'bold'),
                            padx=15, pady=5, relief='raised')
        menu_btn.pack(side='right', padx=10)
        
        # === ОСНОВНАЯ ЧАСТЬ ===
        main_paned = tk.PanedWindow(self.root, bg='#1a2a1a', orient=tk.HORIZONTAL)
        main_paned.pack(fill='both', expand=True, padx=10, pady=5)
        
        # --- ЛЕВАЯ ПАНЕЛЬ: СПИСОК ЛОШАДЕЙ ---
        left_frame = tk.Frame(main_paned, bg='#2a3a2a')
        main_paned.add(left_frame, width=350, minsize=250)
        
        self.horses_list_frame = tk.LabelFrame(left_frame, text="🐴 СПИСОК ЛОШАДЕЙ", bg='#2a3a2a', fg='#FFD700',
                                                font=('Arial', 8, 'bold'))
        self.horses_list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.horses_list_text = tk.Text(self.horses_list_frame, height=20, width=40, bg='#1a2a1a',
                                         font=('Consolas', 9), wrap='word', state='disabled')
        scrollbar1 = tk.Scrollbar(self.horses_list_frame, command=self.horses_list_text.yview)
        self.horses_list_text.configure(yscrollcommand=scrollbar1.set, state='disabled')
        
        self.horses_list_text.tag_configure('gold', foreground='#FFD700')
        self.horses_list_text.tag_configure('white', foreground='#FFFFFF')
        self.horses_list_text.tag_configure('green', foreground='#90EE90')
        self.horses_list_text.tag_configure('red', foreground='#FF6666')
        self.horses_list_text.tag_configure('blue', foreground='#88AAFF')
        self.horses_list_text.tag_configure('gray', foreground='#888888')
        
        scrollbar1.pack(side='right', fill='y')
        self.horses_list_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # --- ПРАВАЯ ПАНЕЛЬ: ПОЛЕ ИГРОКОВ (с прокруткой) ---
        right_container = tk.Frame(main_paned, bg='#1a2a1a')
        main_paned.add(right_container, stretch="always")

        # ✅ ФРЕЙМ ДЛЯ CANVAS
        canvas_frame = tk.Frame(right_container, bg='#1a2a1a')
        canvas_frame.pack(fill='both', expand=True)

        # Canvas
        self.fields_canvas = tk.Canvas(canvas_frame, bg='#1a2a1a', highlightthickness=0)

        # Скроллы
        scrollbar_y = tk.Scrollbar(canvas_frame, orient="vertical", command=self.fields_canvas.yview)
        scrollbar_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.fields_canvas.xview)

        # ✅ КОНТЕЙНЕР ДЛЯ КАРТОЧЕК С ФИКСИРОВАННОЙ ШИРИНОЙ
        CARD_WIDTH = 700
        CARD_SPACING = 20
        CONTAINER_WIDTH = CARD_WIDTH * 2 + CARD_SPACING * 3

        self.fields_frame = tk.Frame(self.fields_canvas, bg='#1a2a1a', width=CONTAINER_WIDTH)
        self.fields_frame.pack_propagate(False)

        self.fields_canvas.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.fields_canvas_window = self.fields_canvas.create_window(
            (0, 0), 
            window=self.fields_frame, 
            anchor="nw"
        )

        # ✅ РАЗМЕЩАЕМ ЧЕРЕЗ GRID
        self.fields_canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, columnspan=2, sticky='ew')

        # ✅ НАСТРАИВАЕМ ВЕСА
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(1, weight=0)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(1, weight=0)

        # ✅ ФУНКЦИЯ ОБНОВЛЕНИЯ ОБЛАСТИ ПРОКРУТКИ
        def configure_fields_frame(event):
            self.fields_canvas.configure(scrollregion=self.fields_canvas.bbox("all"))

        self.fields_frame.bind("<Configure>", configure_fields_frame)

        # ✅ ПРИ ИЗМЕНЕНИИ РАЗМЕРА CANVAS
        def on_canvas_configure(event):
            self.fields_canvas.configure(scrollregion=self.fields_canvas.bbox("all"))

        self.fields_canvas.bind("<Configure>", on_canvas_configure)

        # ============================================================
        # ✅ УПРАВЛЕНИЕ ПРОКРУТКОЙ КОЛЕСИКОМ МЫШИ
        # ============================================================

        # 1. На Canvas - вертикальная прокрутка
        def on_canvas_enter(event):
            def on_mousewheel_for_y(e):
                self.fields_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
            
            # Удаляем старую привязку если есть
            if hasattr(self.fields_canvas, '_wheel_binding'):
                canvas_frame.unbind_all("<MouseWheel>")
            
            self.fields_canvas._wheel_binding = on_mousewheel_for_y
            canvas_frame.bind_all("<MouseWheel>", on_mousewheel_for_y)

        def on_canvas_leave(event):
            if hasattr(self.fields_canvas, '_wheel_binding'):
                canvas_frame.unbind_all("<MouseWheel>")
                delattr(self.fields_canvas, '_wheel_binding')
            # Возвращаем вертикальную прокрутку для всех остальных

        self.fields_canvas.bind("<Enter>", on_canvas_enter)
        self.fields_canvas.bind("<Leave>", on_canvas_leave)

        # 2. На горизонтальном скролле - горизонтальная прокрутка
        def on_scrollbar_x_enter(event):
            def on_mousewheel_for_x(e):
                self.fields_canvas.xview_scroll(int(-1*(e.delta/120)), "units")
            
            # Удаляем старую привязку если есть
            if hasattr(scrollbar_x, '_wheel_binding'):
                canvas_frame.unbind_all("<MouseWheel>")
            
            scrollbar_x._wheel_binding = on_mousewheel_for_x
            canvas_frame.bind_all("<MouseWheel>", on_mousewheel_for_x)

        def on_scrollbar_x_leave(event):
            if hasattr(scrollbar_x, '_wheel_binding'):
                canvas_frame.unbind_all("<MouseWheel>")
                delattr(scrollbar_x, '_wheel_binding')
            # Возвращаем вертикальную прокрутку для Canvas

        scrollbar_x.bind("<Enter>", on_scrollbar_x_enter)
        scrollbar_x.bind("<Leave>", on_scrollbar_x_leave)

        # 3. Shift+Колесо для горизонтальной прокрутки (на любом участке)
        def on_shift_mousewheel(event):
            self.fields_canvas.xview_scroll(int(-1*(event.delta/120)), "units")

        def on_shift_enter(event):
            self.fields_canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)

        def on_shift_leave(event):
            self.fields_canvas.unbind_all("<Shift-MouseWheel>")

        self.fields_canvas.bind("<Enter>", on_shift_enter)
        self.fields_canvas.bind("<Leave>", on_shift_leave)
        
        # === НИЖНЯЯ ПАНЕЛЬ: ДЕЙСТВИЯ + ЖУРНАЛ ===
        bottom_frame = tk.Frame(self.root, bg='#1a2a1a', height=220)
        bottom_frame.pack(fill='x', padx=10, pady=5)
        bottom_frame.pack_propagate(False)
        
        # ДЕЙСТВИЯ (с прокруткой)
        actions_container = tk.Frame(bottom_frame, bg='#1a2a1a', width=220)
        actions_container.pack(side='left', fill='y', padx=5, pady=5)
        actions_container.pack_propagate(False)
        
        self.actions_frame = tk.LabelFrame(actions_container, text="⚡ ДЕЙСТВИЯ", bg='#2a3a2a', fg='#FFD700',
                                      font=('Arial', 12, 'bold'))
        self.actions_frame.pack(fill='both', expand=True)
        
        # Скролл для действий
        actions_canvas = tk.Canvas(self.actions_frame, bg='#2a3a2a', highlightthickness=0)
        actions_scrollbar = tk.Scrollbar(self.actions_frame, orient="vertical", command=actions_canvas.yview)
        self.actions_inner = tk.Frame(actions_canvas, bg='#2a3a2a')
        
        actions_canvas.configure(yscrollcommand=actions_scrollbar.set)
        self.actions_canvas_window = actions_canvas.create_window((0, 0), window=self.actions_inner, anchor="nw")
        
        def configure_actions_inner(event):
            actions_canvas.configure(scrollregion=actions_canvas.bbox("all"))
            actions_canvas.itemconfig(self.actions_canvas_window, width=actions_canvas.winfo_width())
        
        self.actions_inner.bind("<Configure>", configure_actions_inner)
        actions_canvas.bind("<Configure>", lambda e: configure_actions_inner(e))
        
        actions_canvas.pack(side='left', fill='both', expand=True)
        actions_scrollbar.pack(side='right', fill='y')
        
        # ЖУРНАЛ СОБЫТИЙ
        log_frame = tk.LabelFrame(bottom_frame, text="📜 ЖУРНАЛ СОБЫТИЙ", bg='#2a3a2a', fg='#FFD700',
                                  font=('Arial', 12, 'bold'))
        log_frame.pack(side='right', fill='both', expand=True, padx=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=55, bg='#1a2a1a', fg='#90EE90',
                                font=('Consolas', 10), wrap='word', state='disabled')
        scrollbar2 = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar2.set, state='disabled')
        scrollbar2.pack(side='right', fill='y')
        self.log_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.apply_hover_effect_to_all_buttons(self.root)
        
        # Обновляем кнопки
        self.update_actions_buttons()
    
    def update_splash_gif_size(self):
        """Обновляет размер GIF под текущее окно"""
        if not hasattr(self, 'splash_frames') or not self.splash_frames:
            return
        
        try:
            # Получаем текущий размер окна
            self.root.update_idletasks()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # Получаем оригинальный размер GIF
            gif_dir = Path(resource_path("gif"))
            gif_path = gif_dir / "splash.gif"
            
            if not gif_path.exists():
                return
            
            # Открываем оригинальный GIF для получения размеров
            with Image.open(gif_path) as gif:
                original_width, original_height = gif.size
            
            # Доступное пространство (левая часть)
            available_width = int(window_width * 0.40) - 40
            available_height = int(window_height * 0.85) - 40
            
            # Рассчитываем размер с сохранением пропорций
            scale_w = available_width / original_width
            scale_h = available_height / original_height
            scale = min(scale_w, scale_h)
            
            target_width = int(original_width * scale)
            target_height = int(original_height * scale)
            
            # Минимальный размер
            min_size = 200
            if target_width < min_size or target_height < min_size:
                target_width = max(min_size, target_width)
                target_height = int(original_height * (target_width / original_width))
            
            print(f"📐 Обновление GIF: {target_width}x{target_height}")
            
            # Загружаем все кадры с новым размером
            new_frames = []
            with Image.open(gif_path) as gif:
                for frame in ImageSequence.Iterator(gif):
                    frame_copy = frame.copy().resize((target_width, target_height), Image.Resampling.LANCZOS)
                    new_frames.append(ImageTk.PhotoImage(frame_copy))
            
            # Обновляем кадры
            self.splash_frames = new_frames
            self.current_splash_frame = 0
            
            # Обновляем отображение
            if hasattr(self, 'splash_label') and self.splash_label and self.splash_label.winfo_exists():
                if self.splash_frames:
                    self.splash_label.config(image=self.splash_frames[0])
                    
        except Exception as e:
            print(f"Ошибка обновления GIF: {e}")

    def update_actions_buttons(self):
        # ✅ ОЧИЩАЕМ ВНУТРЕННИЙ ФРЕЙМ
        for widget in self.actions_inner.winfo_children():
            widget.destroy()
        
        # ✅ УМЕНЬШАЕМ ВЫСОТУ КНОПОК
        if self.race_mode:
            actions = [
                ("🏇 УЧАСТВОВАТЬ", self.race_participate_action, '#4a7a2e'),
                ("❌ ПРОПУСТИТЬ", self.skip_race_action, '#8B4513')
            ]
            for text, cmd, color in actions:
                btn = tk.Button(self.actions_inner, text=text, command=lambda c=cmd: self.play_and_execute(c),
                               bg=color, fg='white', font=('Arial', 9, 'bold'), 
                               padx=10, pady=4, relief='raised')
                btn.pack(pady=2, fill='x', padx=5)
        elif self.auction_mode:
            actions = [
                ("🏪 РЫНОК", self.market_action, '#4a7a2e'),
                ("⏭ ЗАВЕРШИТЬ ХОД", self.end_auction_turn, '#8B4513')
            ]
            for text, cmd, color in actions:
                btn = tk.Button(self.actions_inner, text=text, command=lambda c=cmd: self.play_and_execute(c),
                               bg=color, fg='white', font=('Arial', 9, 'bold'), 
                               padx=10, pady=4, relief='raised')
                btn.pack(pady=2, fill='x', padx=5)
        else:
            actions = [
                ("🏪 РЫНОК", self.market_action, '#4a7a2e'),
                ("🏇 ТРЕНИРОВКА", self.train_action, '#4a7a2e'),
                ("🎰 ЛОТЕРЕЯ", self.lottery_action, '#4a7a2e'),
                ("🌾 ПОСАДИТЬ", self.plant_radishes_action, '#4a7a2e'),
                ("⏭ ЗАВЕРШИТЬ ХОД", self.end_turn, '#8B4513')
            ]
            for text, cmd, color in actions:
                btn = tk.Button(self.actions_inner, text=text, command=lambda c=cmd: self.play_and_execute(c),
                               bg=color, fg='white', font=('Arial', 9, 'bold'), 
                               padx=10, pady=4, relief='raised')
                btn.pack(pady=2, fill='x', padx=5)
        
        self.apply_hover_effect_to_all_buttons(self.actions_inner)
        
    def race_participate_action(self):
        player = self.players[self.current_player_idx]
        
        if player.action_taken:
            self.show_message("Ошибка", "Вы уже сделали выбор в этом ходу!", "warning")
            return
        
        if not player.horses:
            self.show_message("Ошибка", "Нет лошадей для участия в скачках!", "warning")
            return
        
        if player.gold_quarters < PRICE_RACE_ENTRY:
            self.sound.play('nomoney')
            self.show_message("Ошибка", f"Не хватает денег! Нужно {PRICE_RACE_ENTRY//QUARTERS_PER_GOLD} золотая", "warning")
            return
        
        # Все лошади (и свои, и временные) доступны для участия
        available_horses = [(i, h) for i, h in enumerate(player.horses)]
        
        if not available_horses:
            self.show_message("Ошибка", "Нет доступных лошадей для участия в скачках!", "warning")
            return
        
        # Получаем последнюю участвовавшую лошадь
        last_horse_name = self.last_race_horse.get(player.name, None)
        
        # Фильтруем лошадей - нельзя участвовать той же лошадью дважды подряд (для всех)
        filtered_horses = [(idx, horse) for idx, horse in available_horses if horse.name != last_horse_name]
        
        if not filtered_horses:
            self.show_message("Ошибка", "Все ваши лошади уже участвовали в прошлых скачках! Нужно купить новую лошадь.", "warning")
            return
        
        # Создаём диалог выбора лошади
        horse_dialog = tk.Toplevel(self.root)
        horse_dialog.title("ВЫБОР ЛОШАДИ ДЛЯ СКАЧЕК")
        horse_dialog.geometry("1200x400")
        horse_dialog.configure(bg='#2a3a2a')
        horse_dialog.transient(self.root)
        horse_dialog.grab_set()
        
        tk.Label(horse_dialog, text="Выберите лошадь для участия в скачках:", 
                font=('Arial', 14, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        # Canvas для прокрутки
        canvas = tk.Canvas(horse_dialog, bg='#2a3a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(horse_dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a3a2a')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        for idx, horse in filtered_horses:
            frame = tk.Frame(scrollable_frame, bg='#3a4a3a', relief='ridge', bd=2)
            frame.pack(fill='x', pady=5, padx=10)
            
            # Левая часть с информацией
            info_frame = tk.Frame(frame, bg='#3a4a3a')
            info_frame.pack(side='left', padx=15, pady=10)
            
            # Добавляем метку, если это временная лошадь
            temp_tag = "🔵 (ОПЕКА) " if horse.is_temp else "🟤 "
            
            tk.Label(info_frame, text=f"{temp_tag}{horse.icon} {horse.name} (Ур.{horse.level}) | Скорость: {horse.total_speed} | Прокачки: ", 
                    font=('Arial', 12), bg='#3a4a3a', fg='white' if not horse.is_temp else '#FFD700').pack(side='left')
            
            # Используем универсальную функцию для отображения прокачек
            upgrades_frame = self.create_upgrades_display(info_frame, horse, font_size=12, bg_color='#3a4a3a')
            upgrades_frame.pack(side='left')
            
            # Если это временная лошадь с заданием win_race, показываем напоминание
            if horse.is_temp and player.temp_horse and player.temp_horse.task_type == "win_race" and player.temp_horse.horse.name == horse.name:
                tk.Label(frame, text="🏆 ЗАДАНИЕ: ПОБЕДИТЬ!", 
                        font=('Arial', 10, 'bold'), bg='#3a4a3a', fg='#FFD700').pack(side='left', padx=10)
            
            btn = tk.Button(frame, text="ВЫБРАТЬ", 
                           command=lambda h=horse, d=horse_dialog: self.confirm_race_participation(h, d),
                           bg='#4a7a2e', fg='white', font=('Arial', 11, 'bold'), padx=20)
            btn.pack(side='right', padx=15)
        
        tk.Button(horse_dialog, text="ОТМЕНА", command=horse_dialog.destroy,
                 bg='#8B4513', fg='white', font=('Arial', 12), padx=20).pack(pady=20)
        self.apply_hover_effect_to_all_buttons(horse_dialog)

    def confirm_race_participation(self, horse, dialog):
        player = self.players[self.current_player_idx]
        player.gold_quarters -= PRICE_RACE_ENTRY
        self.race_participants.append((player, horse))
        self.last_race_horse[player.name] = horse.name
        
        # Если у игрока есть временная лошадь и это та же лошадь
        if player.temp_horse and player.temp_horse.horse.name == horse.name:
            player.temp_horse.race_participated = True
            player.temp_horse.race_skipped_by_owner = False
            if player.temp_horse.task_type == "win_race":
                self.log_message(f"🏇 {player.name} выставил на скачки временную лошадь {horse.name} с заданием на победу!")
        else:
            if player.temp_horse and player.temp_horse.horse.name != horse.name:
                player.temp_horse.race_participated = False
                player.temp_horse.race_skipped_by_owner = True  # ШТРАФ!
                if player.temp_horse.task_type == "win_race":
                    self.log_message(f"⚠️ {player.name} выставил на скачки {horse.name}, но задание 'Победа' для {player.temp_horse.horse.name}! Это считается отказом!")
            else:
                self.log_message(f"🏇 {player.name} участвует в скачках с {horse.name}")
        
        self.show_toast(f"{player.name} будет участвовать в скачках с {horse.name}!", "🏇", 3000)
        
        player.action_taken = True
        dialog.destroy()
        self.update_display()
        
        self.current_player_idx += 1
        if self.current_player_idx >= len(self.players):
            self.current_player_idx = 0
            self.run_races()
        else:
            self.update_display()
    
    def skip_race_action(self):
        player = self.players[self.current_player_idx]
        player.action_taken = True
        
        # Если у игрока есть временная лошадь с заданием "win_race"
        if player.temp_horse and player.temp_horse.task_type == "win_race":
            player.temp_horse.race_skipped_by_owner = True  # Отмечаем, что опекун пропустил
            player.temp_horse.race_participated = False
            self.log_message(f"⏭ {player.name} пропускает скачки (есть задание на победу для {player.temp_horse.horse.name})")
        else:
            self.log_message(f"⏭ {player.name} пропускает участие в скачках")
        
        self.update_display()
        
        self.current_player_idx += 1
        if self.current_player_idx >= len(self.players):
            self.current_player_idx = 0
            self.run_races()
        else:
            self.update_display()
    
    def end_race_phase(self):
        """Завершает ход текущего игрока в фазе скачек (для ботов)"""
        self.current_player_idx += 1
        if self.current_player_idx >= len(self.players):
            self.current_player_idx = 0
            self.run_races()
        else:
            self.update_display()
    
    def run_races(self):
        all_players_decided = all(p.action_taken or p.is_bankrupt for p in self.players)
        
        if not all_players_decided:
            return
        
        if len(self.race_participants) >= 2:
            race_dialog = RaceDialog(self.root, self.race_participants, self.sound, self.after_race)
            race_dialog.protocol("WM_DELETE_WINDOW", lambda: None)
            self.root.wait_window(race_dialog)
            if hasattr(race_dialog, 'race_results_info'):
                self.show_race_results_toast(race_dialog.race_results_info)
        else:
            self.log_message("🏇 Недостаточно участников для скачек (нужно минимум 2)")
            
            text_m = ""
            # Возвращаем деньги участникам
            for player, _ in self.race_participants:
                player.gold_quarters += PRICE_RACE_ENTRY
                text_m1 = f"{player.name} возвращена плата за участие в скачках"
                self.log_message(text_m1)
                text_m += text_m1+"\n"
            self.show_toast(text_m, "💰", 4000)
            
            # ✅ ИСПРАВЛЕНО: Проверяем задания win_race ДО того как сбросить флаги
            for player in self.players:
                if player.temp_horse and player.temp_horse.task_type == "win_race":
                    # Если игрок пропустил скачки (отказался) - это штраф
                    if player.temp_horse.race_skipped_by_owner:
                        # Уже отмечено как пропуск, оставляем как есть
                        pass
                    # Если игрок НЕ участвовал и НЕ пропускал (скачки не состоялись по другой причине)
                    elif not player.temp_horse.race_participated:
                        # Скачки не состоялись не по вине опекуна
                        player.temp_horse.race_skipped_by_owner = False
                        player.temp_horse.race_participated = False
            
            self.finish_race_phase()

    def show_race_results_toast(self, results_info):
        """Показывает всплывающее сообщение с результатами скачек"""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.configure(bg='#2a3a2a', relief='ridge', bd=3)
        
        toast.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + 150
        toast.geometry(f"500x150+{x}+{y}")
        
        # Добавляем анимацию появления
        toast.attributes('-alpha', 0)
        
        frame = tk.Frame(toast, bg='#2a3a2a')
        frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        tk.Label(frame, text="🏆 РЕЗУЛЬТАТЫ СКАЧЕК 🏆", 
                font=('Arial', 14, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=5)
        
        tk.Label(frame, text=results_info, font=('Arial', 11),
                bg='#2a3a2a', fg='white', justify='center').pack(pady=5)
        
        # Плавное появление
        def fade_in(alpha=0):
            if alpha <= 0.95:
                alpha += 0.05
                toast.attributes('-alpha', alpha)
                toast.after(30, lambda: fade_in(alpha))
            else:
                toast.after(4000, fade_out)
        
        def fade_out(alpha=0.95):
            if alpha > 0:
                alpha -= 0.05
                toast.attributes('-alpha', alpha)
                toast.after(30, lambda: fade_out(alpha))
            else:
                toast.destroy()
        
        fade_in()

    def process_task_rewards(self):
        """Выдает награды и штрафы за задания после скачек"""
        self.log_message("=" * 30)
        self.log_message("📋 ОБРАБОТКА ЗАДАНИЙ (НАГРАДЫ/ШТРАФЫ)")
        
        task_names = {
            "care": "содержание",
            "train": "тренировка",
            "win_race": "победа в скачках"
        }
        
        for player in self.players:
            if player.temp_horse:
                temp = player.temp_horse
                task_name = task_names.get(temp.task_type, temp.task_type)
                self.log_message(f"🔍 Проверка задания у {player.name}: {temp.horse.name} ({task_name})")
                
                # ========== ЗАДАНИЕ "СОДЕРЖАНИЕ" ==========
                if temp.task_type == "care":
                    # ✅ СНАЧАЛА ПРОВЕРЯЕМ, ЖИВА ЛИ ЛОШАДЬ
                    horse_alive = False
                    for horse in player.horses:
                        if horse.name == temp.horse.name and horse.is_temp:
                            horse_alive = True
                            break
                    
                    # Устанавливаем статус задания
                    if horse_alive:
                        temp.completed = True
                    else:
                        temp.completed = False
                    
                    # ✅ ТЕПЕРЬ ВЫДАЕМ НАГРАДУ ИЛИ ШТРАФ
                    if temp.completed and temp.reward_on_complete > 0 and temp.weeks_left <= 0:
                        # НАГРАДА
                        player.gold_quarters += temp.reward_on_complete
                        reward_gold = temp.reward_on_complete // QUARTERS_PER_GOLD
                        reward_q = temp.reward_on_complete % QUARTERS_PER_GOLD
                        
                        if reward_q > 0:
                            reward_str = f"{reward_gold}.{reward_q} зол."
                        else:
                            reward_str = f"{reward_gold} зол."
                        
                        self.log_message(f"✅ {player.name} ВЫПОЛНИЛ задание 'Содержание' для {temp.horse.name}! Лошадь выжила неделю. Награда: +{reward_str}")
                        self.show_toast(f"Задание 'Содержание' выполнено! {temp.horse.name} выжил. +{reward_str}", "✅", 5000)
                        temp.reward_on_complete = 0
                    
                    elif (not temp.completed and temp.weeks_left <= 0) and temp.advance > 0 and temp.advance_paid:
                        # ШТРАФ
                        player.gold_quarters -= temp.advance
                        penalty_gold = temp.advance // QUARTERS_PER_GOLD
                        penalty_q = temp.advance % QUARTERS_PER_GOLD
                        
                        if penalty_q > 0:
                            penalty_str = f"{penalty_gold}.{penalty_q} зол."
                        else:
                            penalty_str = f"{penalty_gold} зол."
                        
                        self.log_message(f"❌ {player.name} НЕ ВЫПОЛНИЛ задание 'Содержание' для {temp.horse.name}! Лошадь погибла. ШТРАФ: -{penalty_str}")
                        self.show_toast(f"Задание 'Содержание' провалено! {temp.horse.name} погиб. Штраф: -{penalty_str}", "❌", 5000)
                        temp.advance = 0
                    
                    # Если неделя еще не прошла - ничего не делаем
                    elif temp.weeks_left > 0:
                        self.log_message(f"⏳ {player.name}: задание 'Содержание' для {temp.horse.name} еще не завершено (осталось {temp.weeks_left} недель)")
                
                # ========== ЗАДАНИЕ "ТРЕНИРОВКА" ==========
                elif temp.task_type == "train":
                    current_total_upgrades = len(temp.horse.upgrades) + temp.horse.pending_upgrades
                    
                    if hasattr(temp, 'start_total_upgrades'):
                        start_total_upgrades = temp.start_total_upgrades
                    else:
                        start_total_upgrades = temp.start_pending_upgrades
                    
                    gained_upgrades = current_total_upgrades - start_total_upgrades
                    is_max = current_total_upgrades >= TRAINING_UPGRADES_MAX
                    
                    self.log_message(f"📊 {temp.horse.name}: было прокачек {start_total_upgrades}, стало {current_total_upgrades}, получено {gained_upgrades}, максимум: {is_max}")
                    
                    if (gained_upgrades > 0 or is_max):
                        # ✅ Берем награду за тренировку из структуры
                        level = temp.horse.level
                        level_data = HORSE_LEVELS.get(level, HORSE_LEVELS[1])
                        reward_per_upgrade = level_data['rewards']['train']
                        
                        total_reward = reward_per_upgrade * gained_upgrades
                        
                        player.gold_quarters += total_reward
                        reward_gold = total_reward // QUARTERS_PER_GOLD
                        reward_q = total_reward % QUARTERS_PER_GOLD
                        
                        if reward_q > 0:
                            reward_str = f"{reward_gold}.{reward_q} зол."
                        else:
                            reward_str = f"{reward_gold} зол."
                        
                        self.log_message(f"✅ {player.name} ВЫПОЛНИЛ задание 'Тренировка' для {temp.horse.name} Ур. {temp.horse.level}! Получено {gained_upgrades} новых прокачек. Награда: +{reward_str}")
                        self.show_toast(f"Задание 'Тренировка' выполнено! +{gained_upgrades} новых прокачек! +{reward_str}", "✅", 5000)
                        
                        temp.completed = True
                        temp.reward_on_complete = 0
                    
                    # ✅ Штраф ТОЛЬКО если неделя прошла И нет прогресса
                    elif temp.weeks_left <= 0 and gained_upgrades == 0 and not is_max and temp.advance > 0 and temp.advance_paid:
                        player.gold_quarters -= temp.advance
                        penalty_gold = temp.advance // QUARTERS_PER_GOLD
                        penalty_q = temp.advance % QUARTERS_PER_GOLD
                        
                        if penalty_q > 0:
                            penalty_str = f"{penalty_gold}.{penalty_q} зол."
                        else:
                            penalty_str = f"{penalty_gold} зол."
                        
                        self.log_message(f"❌ {player.name} НЕ ВЫПОЛНИЛ задание 'Тренировка' для {temp.horse.name} Ур. {temp.horse.level}! Не получено ни одной новой прокачки за неделю. ШТРАФ: -{penalty_str}")
                        self.show_toast(f"Задание 'Тренировка' провалено! Нет новых прокачек. Штраф: -{penalty_str}", "❌", 5000)
                        
                        temp.advance = 0
                    
                    # ✅ Если неделя еще не прошла - ничего не делаем
                    elif temp.weeks_left > 0:
                        self.log_message(f"⏳ {player.name}: задание 'Тренировка' для {temp.horse.name} Ур. {temp.horse.level} еще не завершено (осталось {temp.weeks_left} недель)")
                
                # ========== ЗАДАНИЕ "ПОБЕДА В СКАЧКАХ" ==========
                elif temp.task_type == "win_race":
                    if temp.race_won and temp.reward_on_complete > 0:
                        temp.completed = True
                        player.gold_quarters += temp.reward_on_complete
                        reward_gold = temp.reward_on_complete // QUARTERS_PER_GOLD
                        reward_q = temp.reward_on_complete % QUARTERS_PER_GOLD
                        reward_str = f"{reward_gold}.{reward_q}" if reward_q > 0 else f"{reward_gold}"
                        self.log_message(f"✅ {player.name} ВЫПОЛНИЛ задание 'Победа в скачках' для {temp.horse.name} Ур. {temp.horse.level}! Победа! Награда: +{reward_str} зол.")
                        self.show_toast(f"Задание 'Победа в скачках' выполнено! {temp.horse.name} победил! +{reward_str} зол.", "✅", 5000)
                        temp.reward_on_complete = 0
                    
                    elif temp.race_participated and temp.advance > 0 and temp.advance_paid:
                        temp.completed = False
                        player.gold_quarters -= temp.advance
                        penalty_gold = temp.advance // QUARTERS_PER_GOLD
                        penalty_q = temp.advance % QUARTERS_PER_GOLD
                        penalty_str = f"{penalty_gold}.{penalty_q}" if penalty_q > 0 else f"{penalty_gold}"
                        self.log_message(f"❌ {player.name} НЕ ВЫПОЛНИЛ задание 'Победа в скачках' для {temp.horse.name} Ур. {temp.horse.level}! Участвовал, но проиграл. ШТРАФ: -{penalty_str} зол.")
                        self.show_toast(f"Задание 'Победа в скачках' провалено! {temp.horse.name} проиграл. Штраф: -{penalty_str} зол.", "❌", 5000)
                        temp.advance = 0
                    
                    elif temp.race_skipped_by_owner and temp.advance > 0 and temp.advance_paid:
                        temp.completed = False
                        player.gold_quarters -= temp.advance
                        penalty_gold = temp.advance // QUARTERS_PER_GOLD
                        penalty_q = temp.advance % QUARTERS_PER_GOLD
                        penalty_str = f"{penalty_gold}.{penalty_q}" if penalty_q > 0 else f"{penalty_gold}"
                        self.log_message(f"❌ {player.name} НЕ ВЫПОЛНИЛ задание 'Победа в скачках' для {temp.horse.name} Ур. {temp.horse.level}! Опекун пропустил скачки. ШТРАФ: -{penalty_str} зол.")
                        self.show_toast(f"Задание 'Победа в скачках' провалено! Вы пропустили скачки. Штраф: -{penalty_str} зол.", "❌", 5000)
                        temp.advance = 0
                    
                    elif not temp.race_participated and not temp.race_skipped_by_owner:
                        temp.completed = True
                        self.log_message(f"✅ {player.name} задание 'Победа в скачках' для {temp.horse.name} Ур. {temp.horse.level} завершено без штрафа (скачки не состоялись)")
                        self.show_toast(f"Задание завершено без штрафа (скачки не состоялись)", "✅", 5000)
            
            else:
                if not player.is_bankrupt:
                    pass
        
        self.log_message("=" * 30)

    def return_temp_horses_to_owners(self):
        """Возвращает временных лошадей владельцам и улучшает их"""
        self.log_message("=" * 30)
        self.log_message("🔄 ВОЗВРАТ ЛОШАДЕЙ ВЛАДЕЛЬЦАМ")
        
        for player in self.players:
            if player.temp_horse:
                temp = player.temp_horse
                applied_upgrades = []
                upgrade_count = 0
                
                # ✅ Используем сохранённые ссылки с проверкой
                original_horse = getattr(temp, 'original_horse', None)
                owner = getattr(temp, 'owner', None)
                
                if owner and original_horse:
                    self.log_message(f"🔹 Возврат {temp.horse.name} владельцу {owner.name} от {player.name}")
                    
                    # ✅ ПРОВЕРЯЕМ, БЫЛО ЛИ ЗАДАНИЕ НА ТРЕНИРОВКУ
                    is_train_task = (temp.task_type == "train")
                    
                    # ✅ ПЕРЕДАЁМ ВСЕ ПРОКАЧКИ ОТ ВРЕМЕННОЙ К ОРИГИНАЛЬНОЙ
                    # 1. Копируем все применённые прокачки (цветные) - ВСЕГДА
                    temp_upgrades = temp.horse.upgrades.copy()
                    if temp_upgrades:
                        original_horse.upgrades = temp_upgrades
                        original_horse.upgrade_count = len(temp_upgrades)
                    
                    # 2. Копируем все белые прокачки - ВСЕГДА
                    if temp.horse.pending_upgrades > 0:
                        original_horse.pending_upgrades = temp.horse.pending_upgrades
                    
                    # 3. Копируем прогресс тренировок - ВСЕГДА
                    if temp.horse.training_progress > 0:
                        original_horse.training_progress = temp.horse.training_progress
                    
                    # ✅ УЛУЧШАЕМ ЛОШАДЬ ТОЛЬКО ЕСЛИ БЫЛА ТРЕНИРОВКА
                    if is_train_task and original_horse.pending_upgrades > 0:
                        applied_upgrades, upgrade_count = self.auto_upgrade_horse(original_horse, owner)

                    # ✅ ПОКАЗЫВАЕМ РЕЗУЛЬТАТ ИГРОКУ
                    if upgrade_count > 0:
                        upgrades_text = ", ".join(applied_upgrades)
                        self.show_toast(
                            f"🏇 {owner.name} улучшил лошадь {original_horse.name}!\n"
                            f"Получено улучшений: {upgrade_count}\n"
                            f"Типы: {upgrades_text}",
                            "⚡", 6000
                        )
                        self.log_message(f"⚡ Владелец {owner.name} улучшил лошадь {original_horse.name} ({upgrade_count} улучшений: {upgrades_text})")
                    else:
                        self.log_message(f"ℹ️ Лошадь {original_horse.name} не получила улучшений (нет белых прокачек или достигнут максимум)")
                    
                else:
                    # Если ссылок нет - пытаемся найти по имени (обратная совместимость)
                    owner = None
                    for o in self.horse_owners.values():
                        if o.name == temp.owner_name:
                            owner = o
                            break
                    
                    if owner:
                        found = False
                        for horse in owner.horses:
                            if horse.name == temp.horse.name:
                                applied_upgrades, upgrade_count = self.auto_upgrade_horse(horse, owner)
                                
                                # ✅ ПОКАЗЫВАЕМ РЕЗУЛЬТАТ ИГРОКУ
                                if upgrade_count > 0:
                                    upgrades_text = ", ".join(applied_upgrades)
                                    self.show_toast(
                                        f"🏇 {owner.name} улучшил лошадь {horse.name}!\n"
                                        f"Получено улучшений: {upgrade_count}\n"
                                        f"Типы: {upgrades_text}",
                                        "⚡", 6000
                                    )
                                    self.log_message(f"⚡ Владелец {owner.name} улучшил лошадь {horse.name} ({upgrade_count} улучшений: {upgrades_text})")
                                else:
                                    self.log_message(f"ℹ️ Лошадь {horse.name} не получила улучшений")
                                
                                found = True
                                break
                        
                        if not found:
                            # Если не нашли - создаём новую лошадь у владельца
                            new_horse = Horse(temp.horse.level, temp.horse.name, owner.color, False)
                            new_horse.upgrades = temp.horse.upgrades.copy()
                            new_horse.training_progress = temp.horse.training_progress
                            new_horse.pending_upgrades = temp.horse.pending_upgrades
                            owner.horses.append(new_horse)
                            applied_upgrades, upgrade_count = self.auto_upgrade_horse(new_horse, owner)
                            
                            if upgrade_count > 0:
                                upgrades_text = ", ".join(applied_upgrades)
                                self.show_toast(
                                    f"🏇 {owner.name} создал и улучшил лошадь {new_horse.name}!\n"
                                    f"Получено улучшений: {upgrade_count}\n"
                                    f"Типы: {upgrades_text}",
                                    "⚡", 6000
                                )
                                self.log_message(f"⚡ Создана и улучшена новая лошадь {new_horse.name} у владельца {owner.name} ({upgrade_count} улучшений: {upgrades_text})")
                            else:
                                self.log_message(f"ℹ️ Создана новая лошадь {new_horse.name} у владельца {owner.name} (без улучшений)")
                    else:
                        self.log_message(f"⚠️ Владелец {temp.owner_name} не найден")
                
                # Удаляем временную лошадь у игрока
                self._remove_temp_horse(player)
        
        self.log_message("=" * 30)

    def _remove_temp_horse(self, player):
        """Удаляет временную лошадь у игрока"""
        for pos, idx in list(player.horse_positions.items()):
            if idx == len(player.horses) - 1:
                del player.horse_positions[pos]
                break
        if player.horses:
            player.horses.pop()
        player.temp_horse = None

    def after_race_with_overlay(self, overlay):
        overlay.destroy()
        self.after_race()

    def after_race(self, log_messages=None):
        """Вызывается, когда скачки СОСТОЯЛИСЬ (было 2+ участников)"""
        # Логируем результаты скачек
        if log_messages:
            for msg in log_messages:
                self.log_message(msg)
        
        # ОБЩАЯ ЧАСТЬ для обоих методов
        self._finish_race_common()
        
        # Специфичная для after_race часть уже выполнена в RaceDialog
        # (награды за победу уже выданы в RaceDialog.finish_race())

    def finish_race_phase(self):
        """Вызывается, когда скачки НЕ СОСТОЯЛИСЬ (меньше 2 участников)"""
    
        # Отмечаем, что скачки не состоялись (не по вине опекунов)
        for player in self.players:
            if player.temp_horse and player.temp_horse.task_type == "win_race":
                player.temp_horse.race_participated = False
        
        # ОБЩАЯ ЧАСТЬ для обоих методов
        self._finish_race_common()

    def _finish_race_common(self):
        """Общая логика после завершения скачек (независимо от того, состоялись они или нет)"""
        self.log_message("=" * 30)
        self.log_message("🏁 ЗАВЕРШЕНИЕ СКАЧЕК")
        
        # ✅ УМЕНЬШАЕМ weeks_left ДЛЯ ВСЕХ ЗАДАНИЙ
        for player in self.players:
            if player.temp_horse:
                player.temp_horse.weeks_left -= 1
        
        # 1. СБОР УРОЖАЯ (редиски продают на рынке)
        self.harvest_phase()
        
        # 2. Выдаем награды/штрафы за задания
        self.process_task_rewards()
        
        # 3. Возвращаем временных лошадей владельцам (и улучшаем их)
        self.return_temp_horses_to_owners()
        
        self.update_market_horses()

        # 4. Генерируем задания для следующего аукциона
        self.generate_auction_tasks()
        
        # 5. Запускаем аукцион
        self.race_mode = False
        self.auction_mode = True
        self.current_player_idx = 0
        for player in self.players:
            player.action_taken = False
        self.update_actions_buttons()
        self.show_overlay_message("АУКЦИОН", "Начинается аукцион! Можно покупать/продавать постройки, лошадей и прокачки, брать задания")
        self.update_display()
        
    
    def show_auction_overlay(self):
        if hasattr(self, 'event_overlay') and self.event_overlay:
            self.event_overlay.destroy()
        
        self.event_overlay = tk.Frame(self.fields_frame, bg='#1a1a2e', bd=5, relief='ridge')
        self.event_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        overlay_bg = tk.Frame(self.event_overlay, bg='#000000')
        overlay_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay_bg.configure(bg='#000000')
        self.event_overlay.lower(overlay_bg)
        
        content = tk.Frame(self.event_overlay, bg='#2a3a2a', relief='ridge', bd=3)
        content.place(relx=0.5, rely=0.5, anchor='center', width=700, height=550)
        
        tk.Label(content, text="🏪 АУКЦИОН 🏪", font=('Arial', 24, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=20)
        
        tk.Label(content, text="Можно покупать и продавать постройки, лошадей и прокачки", 
                font=('Arial', 12), bg='#2a3a2a', fg='white').pack(pady=5)
        
        player = self.players[self.current_player_idx]
        tk.Label(content, text=f"Ход игрока: {player.name}", font=('Arial', 16, 'bold'),
                bg='#2a3a2a', fg='#90EE90').pack(pady=10)
        
        gold = player.gold_quarters // QUARTERS_PER_GOLD
        quarter = player.gold_quarters % QUARTERS_PER_GOLD
        tk.Label(content, text=f"💰 Денег: {gold}.{quarter} зол.", font=('Arial', 14),
                bg='#2a3a2a', fg='#FFD700').pack(pady=5)
        
        if player.temp_horse:
            temp_frame = tk.Frame(content, bg='#3a4a3a', relief='ridge', bd=2)
            temp_frame.pack(fill='x', padx=20, pady=10)
            
            task_names = {"care": "содержание", "train": "тренировка", "win_race": "победа в скачках"}
            status = "✅" if player.temp_horse.completed else "⏳"
            tk.Label(temp_frame, text=f"📋 {status} ОПЕКА: {player.temp_horse.horse.name} ({task_names.get(player.temp_horse.task_type, 'опека')}, {player.temp_horse.weeks_left} нед.)", 
                    font=('Arial', 10), bg='#3a4a3a', fg='#FFD700').pack(pady=5)
        
        btn_frame = tk.Frame(content, bg='#2a3a2a')
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="🏪 ОТКРЫТЬ РЫНОК", 
                 command=self.market_from_overlay,
                 bg='#4a7a2e', fg='white', font=('Arial', 14, 'bold'), padx=30, pady=10).pack(pady=10)
        
        tk.Button(btn_frame, text="⏭ ЗАВЕРШИТЬ ХОД НА АУКЦИОНЕ", 
                 command=self.end_auction_from_overlay,
                 bg='#8B4513', fg='white', font=('Arial', 14, 'bold'), padx=30, pady=10).pack(pady=10)
        self.apply_hover_effect_to_all_buttons(content)
    
    def market_from_overlay(self):
        self.market_action()
    
    def end_auction_from_overlay(self):
        player = self.players[self.current_player_idx]
        player.action_taken = True
        self.current_player_idx += 1
        
        if self.current_player_idx >= len(self.players):
            self.current_player_idx = 0
            self.auction_mode = False  # ✅ Сбрасываем режим аукциона
            if self.event_overlay:
                self.event_overlay.destroy()
            self.update_actions_buttons()
            self.next_day()  # Переходим к следующему дню
        else:
            if self.event_overlay:
                self.event_overlay.destroy()
            self.show_auction_overlay()
        
        self.update_display()
    
    def end_auction_turn(self):
        player = self.players[self.current_player_idx]
        player.action_taken = True
        self.current_player_idx += 1
        
        if self.current_player_idx >= len(self.players):
            self.current_player_idx = 0
            self.auction_mode = False
            self.update_actions_buttons()
            # ✅ Проверяем банкротство перед переходом к следующему дню
            self.check_bankruptcy()
            self.next_day()
        else:
            self.update_display()
        
    def show_overlay_message(self, title, message):
        overlay = tk.Toplevel(self.root)
        overlay.overrideredirect(True)
        overlay.configure(bg='#2a3a2a', relief='ridge', bd=3)
        
        overlay.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + 100
        overlay.geometry(f"400x80+{x}+{y}")
        
        tk.Label(overlay, text=title, font=('Arial', 14, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=5)
        tk.Label(overlay, text=message, font=('Arial', 10),
                bg='#2a3a2a', fg='white').pack()
        
        overlay.after(3000, overlay.destroy)
    
    def show_toast(self, message, icon="✅", duration=5000):
        """Показывает всплывающее уведомление в столбец"""
        # ✅ Если менеджер есть, но контейнер был уничтожен - пересоздаем
        if hasattr(self, 'toast_manager'):
            try:
                self.toast_manager.ensure_container_exists()
            except:
                self.toast_manager = None
        
        if not hasattr(self, 'toast_manager') or self.toast_manager is None:
            self.toast_manager = ToastManager(self.root)
        
        self.toast_manager.show_toast(message, icon, duration)
    
    def play_and_execute(self, action):
        self.sound.play('click')
        action()
    
    def open_sound_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("🔊 НАСТРОЙКИ ЗВУКА")
        dialog.geometry("450x480")
        dialog.configure(bg='#2a3a2a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (480 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(dialog, text="🔊 НАСТРОЙКИ ЗВУКА", font=('Arial', 18, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=20)
        
        music_frame = tk.Frame(dialog, bg='#2a3a2a')
        music_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(music_frame, text="🎵 ФОНОВАЯ МУЗЫКА", font=('Arial', 12, 'bold'),
                bg='#2a3a2a', fg='white').pack(anchor='w')
        
        music_var = tk.BooleanVar(value=self.sound.music_enabled)
        music_check = tk.Checkbutton(music_frame, text="Включить музыку", variable=music_var,
                                     bg='#2a3a2a', fg='white', selectcolor='#3a4a3a',
                                     command=lambda: self.toggle_music(music_var.get()))
        music_check.pack(anchor='w', padx=20)
        
        def on_music_volume_change(v):
            vol = int(v) / 100
            self.sound.set_music_volume(vol)
            self.sound.play('click')
        
        music_volume = tk.Scale(music_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                label="Громкость музыки", length=300,
                                command=on_music_volume_change)
        music_volume.set(self.sound.music_volume * 100)
        music_volume.pack(pady=5)
        
        sfx_frame = tk.Frame(dialog, bg='#2a3a2a')
        sfx_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(sfx_frame, text="🎮 ЗВУКИ ЭФФЕКТОВ", font=('Arial', 12, 'bold'),
                bg='#2a3a2a', fg='white').pack(anchor='w')
        
        sfx_var = tk.BooleanVar(value=self.sound.sfx_enabled)
        sfx_check = tk.Checkbutton(sfx_frame, text="Включить звуки", variable=sfx_var,
                                   bg='#2a3a2a', fg='white', selectcolor='#3a4a3a',
                                   command=lambda: self.toggle_sfx(sfx_var.get()))
        sfx_check.pack(anchor='w', padx=20)
        
        def on_sfx_volume_change(v):
            vol = int(v) / 100
            self.sound.set_sfx_volume(vol)
            self.sound.play('click')
        
        sfx_volume = tk.Scale(sfx_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                              label="Громкость эффектов", length=300,
                              command=on_sfx_volume_change)
        sfx_volume.set(self.sound.sfx_volume * 100)
        sfx_volume.pack(pady=5)
        
        tk.Button(dialog, text="ЗАКРЫТЬ", command=dialog.destroy,
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25).pack(pady=20)

        self.apply_hover_effect_to_all_buttons(dialog)
    
    def toggle_music(self, enabled):
        self.sound.music_enabled = enabled
        if enabled:
            self.sound.play_music()
        else:
            self.sound.stop_music()
        self.sound.play('click')
    
    def toggle_sfx(self, enabled):
        self.sound.sfx_enabled = enabled
        self.sound.play('click')
    
    def draw_radishes_on_field(self, parent, radish_positions, has_icon=False):
        """Отрисовывает редиски на поле в виде сетки 2x2 с белыми кругами"""
        frame = tk.Frame(parent, bg='#2a3a2a')
        frame.pack(fill='both', expand=True)
        
        # Размер клетки для редисок
        cell_size = 32
        
        # Создаём контейнер для центрирования
        container = tk.Frame(frame, bg='#2a3a2a')
        container.pack(expand=True)
        
        # Если нужна иконка поля, рисуем её на фоне
        if has_icon:
            # Создаём Canvas для фона с иконкой поля
            bg_canvas = tk.Canvas(container, width=cell_size*2 + 20, height=cell_size*2 + 20,
                                  bg='#2a3a2a', highlightthickness=0)
            bg_canvas.pack()
            # Рисуем иконку поля
            bg_canvas.create_text(cell_size + 10, cell_size + 10, text="🌾", font=('Arial', 32))
            
            # Создаём поверхностный Canvas для редисок
            overlay_canvas = tk.Canvas(container, width=cell_size*2 + 20, height=cell_size*2 + 20,
                                        bg='#2a3a2a', highlightthickness=0)
            overlay_canvas.place(in_=bg_canvas, x=0, y=0)
            
            # Рисуем редиски поверх
            for i in range(2):
                for j in range(2):
                    pos = i * 2 + j
                    x = 10 + j * cell_size + cell_size//2
                    y = 10 + i * cell_size + cell_size//2
                    if pos in radish_positions:
                        overlay_canvas.create_oval(x-10, y-10, x+10, y+10,
                                                   fill='#FFFFFF', outline='#DDDDDD')
                    else:
                        overlay_canvas.create_oval(x-10, y-10, x+10, y+10,
                                                   fill='#444444', outline='#555555')
        else:
            # Обычная отрисовка без фона
            for i in range(2):
                for j in range(2):
                    pos = i * 2 + j
                    cell = tk.Frame(container, bg='#2a3a2a', width=cell_size, height=cell_size)
                    cell.grid(row=i, column=j, padx=3, pady=3)
                    cell.pack_propagate(False)
                    
                    canvas = tk.Canvas(cell, width=cell_size-4, height=cell_size-4,
                                       bg='#2a3a2a', highlightthickness=0)
                    canvas.pack(expand=True)
                    
                    if pos in radish_positions:
                        canvas.create_oval(3, 3, cell_size-7, cell_size-7,
                                           fill='#FFFFFF', outline='#DDDDDD')
                    else:
                        canvas.create_oval(3, 3, cell_size-7, cell_size-7,
                                           fill='#444444', outline='#555555')
        
        return frame
    
    def create_horse_in_cell(self, parent, horse):
        frame = tk.Frame(parent, bg='#2a3a2a')
        frame.pack(fill='both', expand=True)
        
        PERCENT_X = 0.75
        PERCENT_Y = 0.03
        UPGRADES_X = 0.02
        UPGRADES_START_Y = 0.05
        UPGRADES_SPACING = 0.18
        NAME_X = 0.5
        NAME_Y = 0.9
        
        horse_bg = '#88DD88' if not horse.is_temp else '#6A5ACD'
        horse_container = tk.Frame(frame, bg=horse_bg)
        horse_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        total_progress = horse.training_progress + horse.weekly_training_gain
        progress_in_current = total_progress % TRAINING_CIRCLE_MAX
        progress_percent = int((progress_in_current / TRAINING_CIRCLE_MAX) * 100)
        
        img = self.horse_images.get(horse.level)
        if img:
            img_label = tk.Label(horse_container, image=img, bg=horse_bg)
            img_label.image = img
            img_label.pack(pady=2)
        else:
            tk.Label(horse_container, text=horse.icon, font=('Arial', 32), bg=horse_bg).pack(pady=2)
        
        percent_label = tk.Label(horse_container, text=f"{progress_percent}%", font=('Arial', 8, 'bold'),
                                  bg=horse_bg, fg='#000000')
        percent_label.place(relx=PERCENT_X, rely=PERCENT_Y)
        
        upgrade_display = horse.get_upgrade_display()
        for i, u in enumerate(upgrade_display):
            if u == 'speed':
                color = '#FF6666'  # красный
            elif u == 'radish':
                color = '#90EE90'  # зелёный
            elif u == 'water':
                color = '#88AAFF'  # синий
            elif u == 'pending':
                color = '#FFFFFF'  # белый
            else:
                color = '#555555'  # серый
            
            circle_canvas = tk.Canvas(horse_container, width=12, height=12, 
                                      bg=horse_bg, highlightthickness=0)
            circle_canvas.place(relx=UPGRADES_X, rely=UPGRADES_START_Y + (i * UPGRADES_SPACING))
            circle_canvas.create_oval(2, 2, 10, 10, fill=color, outline='black')
        
        # ПРОГРЕСС-БАР (переименовал в progress_canvas, чтобы не конфликтовать)
        progress_canvas = tk.Canvas(horse_container, width=60, height=6, bg='#1a2a1a', highlightthickness=0)
        progress_canvas.pack(pady=2)
        progress_width = (progress_in_current / TRAINING_CIRCLE_MAX) * 60
        progress_canvas.create_rectangle(0, 0, min(60, progress_width), 6, fill='#FFD700')
        
        name_label = tk.Label(horse_container, text=horse.name[:10], font=('Arial', 8, 'bold'),
                              bg='#2a2a2a', fg='#FFD700', relief='ridge', bd=1)
        name_label.place(relx=NAME_X, rely=NAME_Y, anchor='center', relwidth=0.85)
        
        speed_count = sum(1 for u in horse.upgrades if u == 'speed')
        radish_count = sum(1 for u in horse.upgrades if u == 'radish')
        water_count = sum(1 for u in horse.upgrades if u == 'water')
        pending_count = horse.pending_upgrades
        upgrade_info = f"⚡{speed_count} 🥕{radish_count} 💧{water_count} ⚪{pending_count}"
        tk.Label(horse_container, text=upgrade_info, font=('Arial', 6), 
                bg=horse_bg, fg='#000000').pack()
        
        return frame
    
    def open_menu(self):
        if self.menu_window is not None and self.menu_window.winfo_exists():
            self.menu_window.lift()
            return
        
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("🏆 МЕНЮ ИГРЫ 🏆")
        self.menu_window.geometry("450x650")
        self.menu_window.configure(bg='#2a3a2a')
        self.menu_window.transient(self.root)
        self.menu_window.grab_set()
        
        self.menu_window.update_idletasks()
        x = (self.menu_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.menu_window.winfo_screenheight() // 2) - (650 // 2)
        self.menu_window.geometry(f"+{x}+{y}")
        
        tk.Label(self.menu_window, text="🐎 ЛОШАДИ И РЕДИСКИ 🥕", 
                font=('Arial', 20, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=30)
        
        tk.Label(self.menu_window, text="Фермерская стратегия", 
                font=('Arial', 12), bg='#2a3a2a', fg='white').pack(pady=5)
        
        buttons = [
            ("🎮 ПРОДОЛЖИТЬ ИГРУ", self.close_menu, '#4a7a2e'),
            ("💾 СОХРАНИТЬ", self.show_save_dialog, '#4a7a2e'),
            ("📂 ЗАГРУЗИТЬ", self.show_load_dialog, '#4a7a2e'),
            ("🎲 НОВАЯ ИГРА", self.start_new_game, '#6E3E2E'),
            ("🔊 НАСТРОЙКИ ЗВУКА", self.open_sound_settings, '#4a7a2e'),
            ("📖 ПРАВИЛА", self.show_rules, '#6E3E2E'),
            ("ℹ️ ОБ ИГРЕ", self.show_about, '#6E3E2E'),
            ("🚪 ВЫХОД", self.exit_game, '#8B4513')
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(self.menu_window, text=text, command=lambda c=cmd: self.menu_click(c),
                           bg=color, fg='white', font=('Arial', 12, 'bold'), padx=20, pady=8, relief='raised')
            btn.pack(pady=8, padx=30, fill='x')
        
        tk.Label(self.menu_window, text=get_version_string(), font=('Arial', 9), 
                bg='#2a3a2a', fg='gray').pack(side='bottom', pady=10)

        self.apply_hover_effect_to_all_buttons(self.menu_window)
        self.menu_window.protocol("WM_DELETE_WINDOW", self.close_menu)
    
    def show_save_dialog(self):
        dialog = SaveLoadDialog(self.root, self.saves_dir, self.sound, is_load=False)
        self.root.wait_window(dialog)
        if dialog.result:
            self.save_game_to_file(dialog.result)
    
    def save_game_to_file(self, save_name):
        filename = self.saves_dir / f"{save_name}.json"
        
        # Проверяем, действительно ли сейчас аукцион
        is_sunday = (self.current_day - 1) % 7 == 6
        auction_mode_to_save = self.auction_mode and is_sunday
        
        # ✅ СОХРАНЯЕМ ВЕСЬ ЖУРНАЛ СОБЫТИЙ БЕЗ ОГРАНИЧЕНИЯ
        log_content = []
        try:
            # Получаем текущий текст из лога
            log_content = self.log_text.get('1.0', tk.END).strip().split('\n')
            # Удаляем пустые строки
            log_content = [line for line in log_content if line.strip()]
        except:
            log_content = []

        save_data = {
            'version': GAME_VERSION,
            'current_day': self.current_day,
            'week_number': self.week_number,
            'current_player_idx': self.current_player_idx,
            'race_mode': self.race_mode,
            'auction_mode': auction_mode_to_save,
            'race_participants': [],
            'available_tasks': [],
            'tasks_generated': self.tasks_generated,
            'horse_owners': [],
            'players': [],
            'last_race_horse': self.last_race_horse,
            'log': log_content
        }
        
        # СОХРАНЯЕМ ВЛАДЕЛЬЦЕВ ЛОШАДЕЙ
        for owner in self.horse_owners.values():
            owner_data = {
                'name': owner.name,
                'color': owner.color,
                'wealth': owner.wealth,
                'money': owner.money,
                'horses': [],
                'horses_for_sale': []
            }
            for horse in owner.horses:
                owner_data['horses'].append({
                    'level': horse.level,
                    'name': horse.name,
                    'upgrades': horse.upgrades,
                    'training_progress': horse.training_progress,
                    'weekly_training_gain': horse.weekly_training_gain,  # ✅ ДОБАВЛЕНО
                    'pending_upgrades': horse.pending_upgrades,
                    'is_temp': horse.is_temp
                })
            # ✅ Сохраняем лошадей на продажу по имени
            for horse in owner.horses_for_sale:
                owner_data['horses_for_sale'].append(horse.name)
            save_data['horse_owners'].append(owner_data)
            
        # Сохраняем доступные задания с owner_name
        for task in self.available_tasks:
            save_data['available_tasks'].append({
                'horse_level': task['horse'].level,
                'horse_name': task['horse'].name,
                'task_type': task['task_type'],
                'advance': task['advance'],
                'reward': task['reward'],
                'weekly_cost': task['weekly_cost'],
                'taken': task['taken'],
                'owner_name': task['owner_name']
            })
        
        # Сохраняем участников скачек
        if self.race_participants:
            for player, horse in self.race_participants:
                save_data['race_participants'].append((player.name, horse.name))
        
        # СОХРАНЯЕМ ИГРОКОВ
        for player in self.players:
            player_data = {
                'name': player.name,
                'color': player.color,
                'is_bot': player.is_bot,
                'order': player.order,
                'gold_quarters': player.gold_quarters,
                'stables': player.stables,
                'fields': player.fields,
                'water_buckets': player.water_buckets,
                'radishes': player.radishes,
                'land_map': player.land_map,
                'horse_positions': player.horse_positions,
                'radish_positions': player.radish_positions,
                'is_bankrupt': player.is_bankrupt,
                'action_taken': player.action_taken,
                'horses': []
            }
            
            # Сохраняем лошадей игрока
            for horse in player.horses:
                horse_data = {
                    'level': horse.level,
                    'name': horse.name,
                    'upgrades': horse.upgrades,
                    'training_progress': horse.training_progress,
                    'weekly_training_gain': horse.weekly_training_gain,
                    'pending_upgrades': horse.pending_upgrades,
                    'is_temp': horse.is_temp,
                    'temp_task_type': horse.temp_task_type
                }
                player_data['horses'].append(horse_data)
            
            # Сохраняем временную лошадь (задание)
            if player.temp_horse:
                start_pending = getattr(player.temp_horse, 'start_pending_upgrades', 0)
                start_total = getattr(player.temp_horse, 'start_total_upgrades', start_pending)
                
                player_data['temp_horse'] = {
                    'name': player.temp_horse.horse.name,
                    'level': player.temp_horse.horse.level,
                    'task_type': player.temp_horse.task_type,
                    'advance': player.temp_horse.advance,
                    'reward_on_complete': player.temp_horse.reward_on_complete,
                    'owner_name': player.temp_horse.owner_name,
                    'weeks_left': player.temp_horse.weeks_left,
                    'completed': player.temp_horse.completed,
                    'weekly_cost': player.temp_horse.weekly_cost,
                    'advance_paid': player.temp_horse.advance_paid,
                    'race_won': getattr(player.temp_horse, 'race_won', False),
                    'race_participated': getattr(player.temp_horse, 'race_participated', False),  # ✅ ДОБАВЛЕНО
                    'race_skipped_by_owner': getattr(player.temp_horse, 'race_skipped_by_owner', False),  # ✅ ДОБАВЛЕНО
                    'start_pending_upgrades': start_pending,
                    'start_total_upgrades': start_total
                }
            save_data['players'].append(player_data)
        
        # Сохраняем в файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        self.show_toast(f"Игра сохранена как {save_name}", "💾", 4000)

    def reset_horse_owners(self):
        """Полностью сбрасывает всех владельцев лошадей"""
        self.horse_owners = {}
        self.used_horse_names = set()

    def load_game_from_file(self, filepath):
        # ✅ 1. ПОЛНАЯ ОЧИСТКА ПЕРЕД ЗАГРУЗКОЙ
        self.players = []
        self.current_player_idx = 0
        self.race_participants = []
        self.available_tasks = []
        self.tasks_generated = False
        self.last_race_horse = {}
        self.event_overlay = None
        self.auction_mode = False
        self.race_mode = False
        self.warning_shown_today = False
        self.race_participants = []
        
        # ✅ 2. ПОЛНОСТЬЮ СБРАСЫВАЕМ ВЛАДЕЛЬЦЕВ
        self.horse_owners = {}
        self.used_horse_names = set()
        
        # ✅ 3. СОЗДАЁМ ВЛАДЕЛЬЦЕВ ИЗ ГЛОБАЛЬНЫХ СПИСКОВ
        # Используем те же данные, что и в init_horse_owners()
        for name in OWNER_NAMES:
            self.horse_owners[name] = HorseOwner(
                name=name,
                color=OWNER_COLORS.get(name, "#888888"),
                wealth=OWNER_WEALTH.get(name, 2)
            )
        
        # Теперь читаем сохранение
        with open(filepath, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        if save_data.get('version') != GAME_VERSION:
            if not messagebox.askyesno("Версия не совпадает", 
                f"Версия сохранения ({save_data.get('version', 'unknown')}) отличается от текущей ({GAME_VERSION}).\n"
                "Загрузка может работать некорректно. Продолжить?"):
                return
        
        self.current_day = save_data['current_day']
        self.week_number = save_data['week_number']
        self.current_player_idx = save_data['current_player_idx']
        
        # ВОССТАНАВЛИВАЕМ РЕЖИМЫ
        self.race_mode = save_data.get('race_mode', False)
        self.auction_mode = save_data.get('auction_mode', False)
        
        # ПРОВЕРЯЕМ: если сегодня НЕ воскресенье, то аукциона быть не должно
        is_sunday = (self.current_day - 1) % 7 == 6
        if not is_sunday and self.auction_mode:
            self.auction_mode = False
        
        # ✅ 4. ВОССТАНАВЛИВАЕМ ВЛАДЕЛЬЦЕВ ИЗ СОХРАНЕНИЯ
        for owner_data in save_data.get('horse_owners', []):
            owner_name = owner_data['name']
            owner = self.horse_owners.get(owner_name)
            if owner:
                # Очищаем старые данные
                owner.horses = []
                owner.horses_for_sale = []
                owner.money = owner_data.get('money', owner.wealth * 10 * QUARTERS_PER_GOLD)
                
                # Восстанавливаем лошадей
                for h_data in owner_data.get('horses', []):
                    horse = Horse(h_data['level'], h_data['name'], owner.color, False)
                    horse.upgrades = h_data.get('upgrades', [])
                    horse.upgrade_count = len(horse.upgrades)
                    horse.training_progress = h_data.get('training_progress', 0)
                    horse.weekly_training_gain = h_data.get('weekly_training_gain', 0)
                    horse.pending_upgrades = h_data.get('pending_upgrades', 0)
                    owner.horses.append(horse)
                    self.used_horse_names.add(horse.name)
                
                # Восстанавливаем список продажи
                for horse_name in owner_data.get('horses_for_sale', []):
                    for horse in owner.horses:
                        if horse.name == horse_name and horse not in owner.horses_for_sale:
                            owner.horses_for_sale.append(horse)
                            break
        
        # ВОССТАНАВЛИВАЕМ ЗАДАНИЯ АУКЦИОНА
        self.tasks_generated = save_data.get('tasks_generated', False)
        self.available_tasks = []
        
        for task_data in save_data.get('available_tasks', []):
            horse = Horse(task_data['horse_level'], task_data['horse_name'], "#FFD700", True)
            self.used_horse_names.add(horse.name)
            self.available_tasks.append({
                'horse': horse,
                'task_type': task_data['task_type'],
                'advance': task_data['advance'],
                'reward': task_data['reward'],
                'weekly_cost': task_data['weekly_cost'],
                'taken': task_data['taken'],
                'owner_name': task_data.get('owner_name', "Фермер")
            })

        # Если заданий нет - генерируем новые
        if not self.available_tasks:
            self.generate_auction_tasks()
            self.tasks_generated = True
                
        self.players = []
        for p_data in save_data['players']:
            player = Player(p_data['name'], p_data['color'], p_data['is_bot'], p_data.get('order', 0))
            player.gold_quarters = p_data['gold_quarters']
            player.stables = p_data['stables']
            player.fields = p_data['fields']
            player.water_buckets = p_data['water_buckets']
            player.radishes = p_data['radishes']
            player.land_map = p_data['land_map']
            player.horse_positions = {}
            player.radish_positions = {}
            for pos, radishes in p_data['radish_positions'].items():
                player.radish_positions[int(pos)] = radishes
            player.horses = []
            player.temp_horse = None
            player.is_bankrupt = p_data.get('is_bankrupt', False)
            player.action_taken = p_data.get('action_taken', False)
            
            # Восстанавливаем лошадей
            for h_data in p_data['horses']:
                horse = Horse(h_data['level'], h_data['name'], player.color, h_data.get('is_temp', False))
                horse.upgrades = h_data['upgrades']
                horse.upgrade_count = len(h_data['upgrades'])
                horse.training_progress = h_data['training_progress']
                horse.weekly_training_gain = h_data['weekly_training_gain']
                horse.pending_upgrades = h_data['pending_upgrades']
                horse.temp_task_type = h_data.get('temp_task_type')
                player.horses.append(horse)
                self.used_horse_names.add(horse.name)
            
            # Восстанавливаем позиции лошадей
            for pos, horse_idx in p_data['horse_positions'].items():
                if horse_idx < len(player.horses):
                    player.horse_positions[int(pos)] = horse_idx
            
            # Восстанавливаем временную лошадь
            if 'temp_horse' in p_data and p_data['temp_horse']:
                th = p_data['temp_horse']
                horse = Horse(th['level'], th['name'], player.color, True)
                horse.temp_task_type = th['task_type']
                
                # ✅ ДОБАВИТЬ: восстановление прокачек временной лошади
                for h_data in p_data.get('horses', []):
                    if h_data['name'] == th['name'] and h_data.get('is_temp', True):
                        horse.upgrades = h_data.get('upgrades', [])
                        horse.upgrade_count = len(horse.upgrades)
                        horse.training_progress = h_data.get('training_progress', 0)
                        horse.weekly_training_gain = h_data.get('weekly_training_gain', 0)
                        horse.pending_upgrades = h_data.get('pending_upgrades', 0)
                        break
                
                self.used_horse_names.add(horse.name)
                player.temp_horse = TempHorse(horse, th['task_type'], th['advance'], th['reward_on_complete'], 
                                              th['owner_name'], th.get('weekly_cost', 0))
                player.temp_horse.weeks_left = th['weeks_left']
                player.temp_horse.completed = th.get('completed', False)
                player.temp_horse.advance_paid = th.get('advance_paid', False)
                player.temp_horse.race_won = th.get('race_won', False)
                player.temp_horse.race_participated = th.get('race_participated', False)
                player.temp_horse.race_skipped_by_owner = th.get('race_skipped_by_owner', False)
                player.temp_horse.start_pending_upgrades = th.get('start_pending_upgrades', 0)
                player.temp_horse.start_total_upgrades = th.get('start_total_upgrades', th.get('start_pending_upgrades', 0))
                
                # ✅ НАХОДИМ ИЛИ СОЗДАЕМ ОРИГИНАЛЬНУЮ ЛОШАДЬ
                owner = None
                for o in self.horse_owners.values():
                    if o.name == th['owner_name']:
                        owner = o
                        break
                
                if owner:
                    player.temp_horse.owner = owner
                    # Ищем лошадь с таким же именем у владельца
                    found = False
                    for h in owner.horses:
                        if h.name == th['name']:
                            player.temp_horse.original_horse = h
                            found = True
                            break
                    
                    # ✅ ЕСЛИ НЕ НАШЛИ - СОЗДАЕМ НОВУЮ
                    if not found:
                        # Создаем оригинальную лошадь
                        original = Horse(th['level'], th['name'], owner.color, False)
                        # Восстанавливаем прокачки из сохранения
                        for h_data in p_data.get('horses', []):
                            if h_data['name'] == th['name'] and not h_data.get('is_temp', False):
                                original.upgrades = h_data.get('upgrades', [])
                                original.upgrade_count = len(original.upgrades)
                                original.training_progress = h_data.get('training_progress', 0)
                                original.weekly_training_gain = h_data.get('weekly_training_gain', 0)
                                original.pending_upgrades = h_data.get('pending_upgrades', 0)
                                break
                        owner.horses.append(original)
                        player.temp_horse.original_horse = original
                
                # Добавляем временную лошадь в стойло
                free_stable = player.get_free_stable()
                if free_stable != -1:
                    player.horse_positions[free_stable] = len(player.horses)
                    player.horses.append(horse)
            
            self.players.append(player)
        
        # ✅ 5. ВОССТАНАВЛИВАЕМ УЧАСТНИКОВ СКАЧЕК
        if self.race_mode and 'race_participants' in save_data:
            for p_name, horse_name in save_data['race_participants']:
                for player in self.players:
                    if player.name == p_name:
                        for horse in player.horses:
                            if horse.name == horse_name:
                                self.race_participants.append((player, horse))
                                break
                        break
        
        # ✅ 6. ПРОВЕРЯЕМ И КОРРЕКТИРУЕМ РЫНОК
        for owner in self.horse_owners.values():
            # Удаляем дубликаты
            seen = set()
            unique = []
            for h in owner.horses_for_sale:
                if h.name not in seen:
                    seen.add(h.name)
                    unique.append(h)
            owner.horses_for_sale = unique
            
            # Удаляем лошадей, которых нет у владельца
            owner.horses_for_sale = [h for h in owner.horses_for_sale if h in owner.horses]
        
        # ✅ 7. ВОССТАНАВЛИВАЕМ last_race_horse
        self.last_race_horse = save_data.get('last_race_horse', {})
        
        # Принудительно перезагружаем изображения
        self.load_horse_images()
        self.load_horse_gif()
        
        # Пересоздаём UI
        self.create_ui()
        
        # ✅ 8. ВОССТАНАВЛИВАЕМ ВЕСЬ ЖУРНАЛ СОБЫТИЙ
        if 'log' in save_data and save_data['log']:
            self.log_text.config(state='normal')
            self.log_text.delete('1.0', tk.END)
            for line in save_data['log']:
                if line.strip():
                    self.log_text.insert(tk.END, line + '\n')
            self.log_text.see('1.0')
            self.log_text.config(state='disabled')
        
        # Запускаем музыку
        self.sound.play_music()
        
        # Сбрасываем флаг предупреждения
        self.warning_shown_today = False
        
        # Обновляем кнопки действий в соответствии с режимом
        self.update_actions_buttons()
        
        # Обновляем отображение
        self.update_display()
        
        self.show_toast(f"Игра загружена из {filepath.stem}", "📂", 4000)
    
    def close_menu(self):
        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None
    
    def start_new_game(self):
        if messagebox.askyesno("Новая игра", "Начать новую игру? Текущий прогресс будет потерян!"):
            self.close_menu()
            self.sound.stop_music()
            for widget in self.root.winfo_children():
                widget.destroy()
            self.__init__(self.root)
    
    def exit_game(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из игры?"):
            self.sound.stop_music()
            self.root.quit()
    
    def show_rules(self):
        def fill_content(parent):
            # ═══════════════ ЗАГОЛОВОК (ФИКСИРОВАН) ═══════════════
            tk.Label(parent, text="🏆 ПРАВИЛА ИГРЫ 🏆", 
                    font=('Arial', 16, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=(0, 10))
            tk.Frame(parent, bg='#4a7a2e', height=2).pack(fill='x', padx=20, pady=(0, 10))
            
            # ═══════════════ ТЕКСТ С ПРОКРУТКОЙ ═══════════════
            text_frame = tk.Frame(parent, bg='#2a3a2a')
            text_frame.pack(fill='both', expand=True, pady=(0, 10))
            
            canvas = tk.Canvas(text_frame, bg='#2a3a2a', highlightthickness=0)
            scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#2a3a2a')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            def update_canvas_width(event):
                canvas.itemconfig(canvas_window, width=event.width - 10)
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            canvas.bind("<Configure>", update_canvas_width)
            
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
            canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
            
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            
            # ═══════════════ СОДЕРЖИМОЕ С ПРОКРУТКОЙ ═══════════════
            
            # 📅 ЦЕЛЬ ИГРЫ
            tk.Label(scrollable_frame, text="📅 ЦЕЛЬ ИГРЫ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text="Стать самым богатым фермером за 60 дней.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # 💰 КАПИТАЛ
            tk.Label(scrollable_frame, text="💰 КАПИТАЛ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text="Суммарная стоимость всех активов.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # 🏠 ПОСТРОЙКИ
            tk.Label(scrollable_frame, text="🏠 ПОСТРОЙКИ (только в ВОСКРЕСЕНЬЕ):", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text=f"• Стойло ({PRICE_STABLE//QUARTERS_PER_GOLD} золотая) - место для 1 лошади", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text=f"• Поле ({PRICE_FIELD//QUARTERS_PER_GOLD} золотая) - место для 4 редисок", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # 🥕 РЕСУРСЫ
            tk.Label(scrollable_frame, text="🥕 РЕСУРСЫ (можно покупать/продавать в любой день):", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text=f"• Редиска ({PRICE_RADISH} четвертак) - еда для лошадей и для посадки", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text=f"• Вода ({PRICE_WATER} четвертак) - вода для лошадей и для посадки редиски", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # 🐴 ЛОШАДИ (динамически из HORSE_LEVELS)
            tk.Label(scrollable_frame, text="🐴 ЛОШАДИ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            
            for level, data in sorted(HORSE_LEVELS.items()):
                cost_gold = data['cost'] // QUARTERS_PER_GOLD
                cost_q = data['cost'] % QUARTERS_PER_GOLD
                if cost_q > 0:
                    cost_str = f"{cost_gold}.{cost_q} зол."
                else:
                    cost_str = f"{cost_gold} зол."
                
                speed = data['base_speed']
                speed_str = f"+{speed}" if speed > 0 else str(speed)
                
                text = f"• {level} уровень {data['icon']}: скорость {speed_str}, ест {data['base_food']}/пьёт {data['base_water']}, цена {cost_str}"
                tk.Label(scrollable_frame, text=text, 
                        font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # ⚡ ПРОКАЧКИ
            tk.Label(scrollable_frame, text="⚡ ПРОКАЧКИ ЛОШАДИ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            
            upgrades = [
                ("+1 скорость", '#FF4444'),
                ("-1 редиска/день", '#00d632'),
                ("-1 ведро/день", '#4444FF'),
                ("доступно для покупки", '#FFFFFF'),
                ("пустой слот", '#888888'),
            ]
            
            for text, color in upgrades:
                frame = tk.Frame(scrollable_frame, bg='#2a3a2a')
                frame.pack(anchor='w', padx=30, pady=1)
                
                tk.Label(frame, text="⚫", font=('Arial', 10), 
                        bg='#2a3a2a', fg=color).pack(side='left')
                tk.Label(frame, text=f"  {text}", font=('Arial', 10), 
                        bg='#2a3a2a', fg='white').pack(side='left')
            
            # 🏇 ТРЕНИРОВКИ (с наградами из HORSE_LEVELS)
            tk.Label(scrollable_frame, text="🏇 ТРЕНИРОВКИ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text=f"После {TRAINING_CIRCLE_MAX} единиц прогресса (100%) - новый белый слот для прокачки.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text=f"Прокачку можно купить в воскресенье за {PRICE_UPGRADE} четвертак.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # Награды за тренировку
            tk.Label(scrollable_frame, text="Награды за задание «Тренировка» (за каждую прокачку):", 
                    font=('Arial', 10, 'bold'), bg='#2a3a2a', fg='#90EE90', anchor='w').pack(fill='x', padx=30, pady=(5, 1))
            
            for level, data in sorted(HORSE_LEVELS.items()):
                reward = data['rewards']['train']
                reward_gold = reward // QUARTERS_PER_GOLD
                reward_q = reward % QUARTERS_PER_GOLD
                if reward_q > 0:
                    reward_str = f"{reward_gold}.{reward_q} зол."
                else:
                    reward_str = f"{reward_gold} зол."
                
                text = f"  • {level} уровень: {reward_str}"
                tk.Label(scrollable_frame, text=text, 
                        font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=40, pady=1)
            
            # 🌾 РЕДИСКИ
            tk.Label(scrollable_frame, text="🌾 РЕДИСКИ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text="Сажать - только в понедельник (1 вода на редиску).", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="Поливать только в день посадки!", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text=f"На поле помещается до {RADISH_PER_FIELD} редисок.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="Сбор урожая - в воскресенье (цена от 0 до 4 четвертаков).", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # 🏆 СКАЧКИ
            tk.Label(scrollable_frame, text="🏆 СКАЧКИ (воскресенье):", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text=f"Участие - {PRICE_RACE_ENTRY//QUARTERS_PER_GOLD} золотая.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="Призы (в зависимости от количества участников):", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="  • 2 участника: 1 место - 2 зол., 2 место - без награды", 
                    font=('Arial', 10), bg='#2a3a2a', fg='#90EE90', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="  • 3 участника: 1 место - 4 зол., 2 место - 2 зол., 3 место - без награды", 
                    font=('Arial', 10), bg='#2a3a2a', fg='#90EE90', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="  • 4 участника: 1 место - 5 зол., 2 место - 2.2 зол., 3 место - 1 зол., 4 место - без награды", 
                    font=('Arial', 10), bg='#2a3a2a', fg='#90EE90', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # Награды за победу в скачках (из HORSE_LEVELS)
            tk.Label(scrollable_frame, text="Награды по заданию «Победа в скачках» (в зависимости от уровня лошади):", 
                    font=('Arial', 10, 'bold'), bg='#2a3a2a', fg='#90EE90', anchor='w').pack(fill='x', padx=30, pady=(5, 1))
            
            for level, data in sorted(HORSE_LEVELS.items()):
                reward = data['rewards']['win_race']
                reward_gold = reward // QUARTERS_PER_GOLD
                reward_q = reward % QUARTERS_PER_GOLD
                if reward_q > 0:
                    reward_str = f"{reward_gold}.{reward_q} зол."
                else:
                    reward_str = f"{reward_gold} зол."
                
                text = f"  • {level} уровень: {reward_str}"
                tk.Label(scrollable_frame, text=text, 
                        font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=40, pady=1)
                
            tk.Label(scrollable_frame, text="ВНИМАНИЕ: одна и та же лошадь не может участвовать в скачках два раза подряд!", 
                    font=('Arial', 10), bg='#2a3a2a', fg='#FF4444', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # 💀 БАНКРОТСТВО
            tk.Label(scrollable_frame, text="💀 БАНКРОТСТВО и ШТРАФЫ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text="Если капитал игрока становится меньше 0 - игрок выбывает!", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="Штрафы могут увести игрока в минус, и если его активы не покрывают долг - он проигрывает.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='#90EE90', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="Штрафы начисляются на сумму аванса за невыполненное задание.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='#FF4444', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            tk.Label(scrollable_frame, text="За гибель чужой лошади налагается штраф в размере стоимости самой лошади.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='#FF4444', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=1)
            
            # 🎉 ПОБЕДА
            tk.Label(scrollable_frame, text="🎉 ПОБЕДА:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700', anchor='w').pack(fill='x', padx=20, pady=(10, 2))
            tk.Label(scrollable_frame, text="Игрок с наибольшим капиталом после 60 дней или последний оставшийся игрок.", 
                    font=('Arial', 10), bg='#2a3a2a', fg='white', anchor='w', wraplength=650).pack(fill='x', padx=30, pady=(1, 10))
            
            # ═══════════════ ВЕРСИЯ И КНОПКА (ФИКСИРОВАНЫ) ═══════════════
            tk.Frame(parent, bg='#4a7a2e', height=2).pack(fill='x', padx=20, pady=(5, 10))
            
            tk.Label(parent, text=get_version_string(), 
                    font=('Arial', 9), bg='#2a3a2a', fg='gray').pack(pady=(0, 10))
            
            def close_dialog():
                parent.winfo_toplevel().destroy()
            
            tk.Button(parent, text="ЗАКРЫТЬ", command=close_dialog,
                     bg='#8B4513', fg='white', font=('Arial', 11, 'bold'),
                     padx=30, pady=8).pack()
        
        self.create_styled_dialog("📖 ПРАВИЛА ИГРЫ", fill_content, 500, 900, 400, 700)
    
    def show_about(self):
        def fill_content(parent):
            # Заголовок
            tk.Label(parent, text="🐎 Лошади и Редиски 🥕", 
                    font=('Arial', 20, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=(0, 5))
            
            tk.Label(parent, text=get_version_string(), 
                    font=('Arial', 12), bg='#2a3a2a', fg='#90EE90').pack(pady=(0, 15))
            
            tk.Label(parent, text="Фермерская стратегия с элементами RPG.", 
                    font=('Arial', 11), bg='#2a3a2a', fg='white').pack(pady=(0, 15))
            
            # Разделитель
            tk.Frame(parent, bg='#4a7a2e', height=2).pack(fill='x', padx=20, pady=10)
            
            # Информация
            info_texts = [
                "Анимация создана с помощью komiko.app",
                "Звуки игры взяты с zvukipro.com",
                "Изображения созданы с помощью myneuralnetworks.ru и chatgpt.com",
                "Музыка создана с помощью suno.com",
                "Озвучивание создано с помощью topmediai.com",
                "Код игры написан с помощью chat.deepseek.com на Python",
            ]
            
            for text in info_texts:
                tk.Label(parent, text=text, 
                        font=('Arial', 10), bg='#2a3a2a', fg='#C0C0C0').pack(pady=2)
            
            # Разделитель
            tk.Frame(parent, bg='#4a7a2e', height=2).pack(fill='x', padx=20, pady=10)
            
            # Подпись
            tk.Label(parent, text="Приятной игры! 🎮", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=(10, 15))
            
            # Кнопка закрытия
            def close_dialog():
                parent.winfo_toplevel().destroy()
            
            tk.Button(parent, text="ЗАКРЫТЬ", command=close_dialog,
                     bg='#8B4513', fg='white', font=('Arial', 11, 'bold'),
                     padx=30, pady=8).pack()
        
        self.create_styled_dialog("ℹ️ ОБ ИГРЕ", fill_content, 400, 600, 350, 500)
    
    def sync_horse_positions(self, player):
        """
        Синхронизирует horse_positions с актуальным списком лошадей.
        Удаляет позиции, указывающие на несуществующие индексы.
        """
        positions_to_remove = []
        for pos, horse_idx in list(player.horse_positions.items()):
            if horse_idx >= len(player.horses):
                positions_to_remove.append(pos)
        
        for pos in positions_to_remove:
            del player.horse_positions[pos]
            self.log_message(f"⚠️ Синхронизация: удалена позиция {pos} с несуществующей лошадью")
        
        return len(positions_to_remove) > 0

    def update_horses_list(self):
        # ✅ ПРОВЕРКА: существует ли horses_list_text
        try:
            if not self.horses_list_text.winfo_exists():
                return
        except (tk.TclError, AttributeError):
            return
        
        player = self.players[self.current_player_idx]
        self.horses_list_text.config(state='normal')
        self.horses_list_text.delete('1.0', tk.END)
        
        # Настраиваем теги для цветов
        self.horses_list_text.tag_configure('red', foreground='#FF6666')
        self.horses_list_text.tag_configure('green', foreground='#90EE90')
        self.horses_list_text.tag_configure('blue', foreground='#88AAFF')
        self.horses_list_text.tag_configure('white', foreground='#FFFFFF')
        self.horses_list_text.tag_configure('gold', foreground='#FFD700')
        self.horses_list_text.tag_configure('gray', foreground='#888888')
        
        if not player.horses:
            self.horses_list_text.insert('1.0', "🐴 Нет лошадей\n", 'white')
        else:
            for i, horse in enumerate(player.horses, 1):
                total_progress = horse.training_progress + horse.weekly_training_gain
                circles_completed = total_progress // TRAINING_CIRCLE_MAX
                progress_in_current = total_progress % TRAINING_CIRCLE_MAX
                progress_percent = int((progress_in_current / TRAINING_CIRCLE_MAX) * 100)
                price = horse.sell_price()
                
                temp_mark = "🔵 (ОПЕКА) " if horse.is_temp else "🟤 "
                name_color = 'gold' if horse.is_temp else 'white'
                
                self.horses_list_text.insert(tk.END, f"\n{i}. ", name_color)
                self.horses_list_text.insert(tk.END, f"{temp_mark}{horse.icon} {horse.name} (Ур.{horse.level})\n", name_color)
                
                self.horses_list_text.insert(tk.END, f"   🏃 Скорость: ", 'white')
                self.horses_list_text.insert(tk.END, f"{horse.total_speed}\n", 'red')
                
                self.horses_list_text.insert(tk.END, f"   🥕 Ест: ", 'white')
                self.horses_list_text.insert(tk.END, f"{horse.food_per_day} редисок/день\n", 'green')
                
                self.horses_list_text.insert(tk.END, f"   💧 Пьёт: ", 'white')
                self.horses_list_text.insert(tk.END, f"{horse.water_per_day} вёдер/день\n", 'blue')
                
                self.horses_list_text.insert(tk.END, f"   🏋️ Круги: ", 'white')
                self.horses_list_text.insert(tk.END, f"{circles_completed} завершено, {progress_percent}% до следующего\n", 'white')
                
                self.horses_list_text.insert(tk.END, f"   ⭐ Прокачки: ", 'white')
                for text, tag in self.get_upgrades_colored_text(horse):
                    self.horses_list_text.insert(tk.END, text, tag)
                    self.horses_list_text.insert(tk.END, ' ', 'white')
                
                self.horses_list_text.insert(tk.END, '\n', 'white')
                
                if horse.pending_upgrades > 0:
                    self.horses_list_text.insert(tk.END, f"   ⚡ Доступно белых прокачек: {horse.pending_upgrades}\n", 'gold')
                
                self.horses_list_text.insert(tk.END, f"   💰 Стоимость: ", 'white')
                self.horses_list_text.insert(tk.END, f"{price//QUARTERS_PER_GOLD}.{price%QUARTERS_PER_GOLD} зол.\n", 'gold')
        
        self.horses_list_text.config(state='disabled')
    
    def draw_player_farm(self, player, row, col):
        # ✅ ФИКСИРОВАННЫЙ РАЗМЕР КАРТОЧКИ
        CARD_WIDTH = 700
        CARD_HEIGHT = 500
        cell_size = 100
        font_size = 10
        small_font = 7
        title_font = 11
        
        # ✅ КАРТОЧКА С ФИКСИРОВАННЫМ РАЗМЕРОМ
        frame = tk.Frame(self.fields_frame, bg=player.color, relief='ridge', bd=3)
        frame.grid(row=row, column=col, padx=10, pady=10)
        frame.grid_propagate(False)
        frame.config(width=CARD_WIDTH, height=CARD_HEIGHT)
        
        if player.is_bankrupt:
            for widget in frame.winfo_children():
                widget.destroy()
            tk.Label(frame, text="💀 БАНКРОТ 💀", font=('Arial', 20, 'bold'),
                    bg='#333333', fg='#FF4444').pack(expand=True)
            return
        
        # title_frame
        title_frame = tk.Frame(frame, bg=player.color)
        title_frame.pack(fill='x', padx=5, pady=5)
        
        bot_tag = "🤖 " if player.is_bot else ""
        tk.Label(title_frame, text=f"#{player.order} 🏠 {bot_tag}{player.name}", 
                font=('Arial', title_font, 'bold'),
                bg=player.color, fg='#FFD700').pack(side='left')
        
        # Статусы
        if self.race_mode:
            is_participating = any(p == player for p, _ in self.race_participants)
            if player.action_taken:
                if is_participating:
                    status_text = "🏇 УЧАСТВУЕТ"
                    status_color = '#4a7a2e'
                    status_bg = 'white'
                else:
                    status_text = "❌ НЕ УЧАСТВУЕТ"
                    status_color = '#8B4513'
                    status_bg = 'white'
            else:
                if is_participating:
                    status_text = "⏳ ОЖИДАНИЕ"
                    status_color = '#FFD700'
                    status_bg = 'black'
                else:
                    status_text = "⌛ НЕ ОПРЕДЕЛЕНО"
                    status_color = '#888888'
                    status_bg = 'black'
            
            tk.Label(title_frame, text=status_text, font=('Arial', small_font, 'bold'),
                    bg=status_bg, fg=status_color, padx=5).pack(side='right')
        
        elif not self.auction_mode and not player.action_taken and not player.is_bot and self.players.index(player) == self.current_player_idx:
            tk.Label(title_frame, text="▶ ВАШ ХОД ◀", font=('Arial', small_font + 1, 'bold'),
                    bg='#FF4500', fg='white', padx=5).pack(side='right')
        
        elif self.auction_mode and self.players.index(player) == self.current_player_idx:
            if not player.action_taken:
                tk.Label(title_frame, text="🏪 ХОД НА АУКЦИОНЕ", font=('Arial', small_font, 'bold'),
                        bg='#FFD700', fg='black', padx=5).pack(side='right')
        
        # Ресурсы
        resources_bg = tk.Frame(frame, bg='#1a2a1a', relief='sunken', bd=1)
        resources_bg.pack(fill='x', padx=10, pady=5)
        
        gold = player.gold_quarters // QUARTERS_PER_GOLD
        quarter = player.gold_quarters % QUARTERS_PER_GOLD
        capital = player.total_capital
        capital_gold = capital // QUARTERS_PER_GOLD
        capital_q = capital % QUARTERS_PER_GOLD
        
        total_radish_need = sum(h.food_per_day for h in player.horses)
        total_water_need = sum(h.water_per_day for h in player.horses)
        
        # ✅ ФОРМИРУЕМ ПРЕДУПРЕЖДЕНИЕ
        warning_text = ""
        if player.radishes < total_radish_need and player.water_buckets < total_water_need:
            warning_text = "🚨 НЕ ХВАТАЕТ РЕДИСОК И ВОДЫ!"
            
        elif player.radishes < total_radish_need:
            warning_text = "🚨 НЕ ХВАТАЕТ РЕДИСОК!"
            
        elif player.water_buckets < total_water_need:
            warning_text = "🚨 НЕ ХВАТАЕТ ВОДЫ!"
            
        
        # ✅ ОСНОВНАЯ ИНФОРМАЦИЯ
        main_info = tk.Frame(resources_bg, bg='#1a2a1a')
        main_info.pack(fill='x')
        
        tk.Label(main_info, text=f"💰 {gold}.{quarter} зол. | 💎 {capital_gold}.{capital_q} капитал", 
            font=('Arial', font_size, 'bold'), bg='#1a2a1a', 
            fg='#FF4444' if warning_text else '#FFD700').pack(side='left', padx=10, pady=3)
        
        tk.Label(main_info, text=f"🐴 {len([h for h in player.horses if not h.is_temp])} | 🥕 {player.radishes} | 💧 {player.water_buckets}", 
                font=('Arial', font_size), bg='#1a2a1a', fg='white').pack(side='right', padx=10, pady=3)
        
        # ✅ ПРЕДУПРЕЖДЕНИЕ - ОТДЕЛЬНАЯ ЯРКАЯ СТРОКА
        if warning_text:
            warning_frame = tk.Frame(resources_bg, bg='#FF4444', relief='ridge', bd=1)
            warning_frame.pack(fill='x', padx=5, pady=2)
            tk.Label(warning_frame, text=warning_text, font=('Arial', font_size, 'bold'), 
                    bg='#FF4444', fg='white').pack(pady=2)
        
        # Статус задания
        if player.temp_horse:
            temp_frame = tk.Frame(frame, bg='#1a2a1a', relief='ridge', bd=1)
            temp_frame.pack(fill='x', padx=10, pady=5)
            status = "✅" if player.temp_horse.completed else "⏳"
            task_names = {"care": "содержание", "train": "тренировка", "win_race": "победа"}
            task_text = task_names.get(player.temp_horse.task_type, "опека")
            
            if player.temp_horse.task_type == "win_race":
                if player.temp_horse.race_won:
                    status_suffix = "🏆 ПОБЕДА!"
                elif player.temp_horse.race_participated:
                    status_suffix = "❌ ПРОИГРАЛ"
                elif player.temp_horse.race_skipped_by_owner:
                    status_suffix = "⏭ ПРОПУСТИЛ"
                else:
                    status_suffix = "⏳ ОЖИДАНИЕ"
                
                tk.Label(temp_frame, text=f"📋 {status} {player.temp_horse.horse.name} ({task_text})", 
                        font=('Arial', small_font, 'bold'), bg='#1a2a1a', fg='#FFD700').pack()
            else:
                tk.Label(temp_frame, text=f"📋 {status} {player.temp_horse.horse.name} ({task_text}, {player.temp_horse.weeks_left} нед.)", 
                        font=('Arial', small_font, 'bold'), bg='#1a2a1a', fg='#FFD700').pack()
        
        # Сетка с ячейками
        grid_frame = tk.Frame(frame, bg=player.color)
        grid_frame.pack(padx=10, pady=2)
        
        for i in range(MAX_LAND):
            row_grid = i // 5
            col_grid = i % 5
            
            cell_frame = tk.Frame(grid_frame, bg='#1a2a1a', relief='ridge', bd=2, width=cell_size, height=cell_size)
            cell_frame.grid(row=row_grid, column=col_grid, padx=2, pady=2)
            cell_frame.pack_propagate(False)
            
            content_frame = tk.Frame(cell_frame, bg='#2a3a2a')
            content_frame.pack(fill='both', expand=True)
            
            if player.land_map[i] == 1:
                if i in player.horse_positions:
                    horse_idx = player.horse_positions[i]
                    if horse_idx < len(player.horses):
                        horse = player.horses[horse_idx]
                        self.create_horse_in_cell(content_frame, horse)
                else:
                    tk.Label(content_frame, text="🏠", font=('Arial', int(cell_size * 0.35)), bg='#2a3a2a').pack(pady=5)
                    tk.Label(content_frame, text="СВОБОДНО", font=('Arial', small_font), bg='#2a3a2a', fg='gray').pack()
            
            elif player.land_map[i] == 2:
                if i in player.radish_positions:
                    radish_positions = player.radish_positions[i]
                    self.draw_radishes_on_field(content_frame, radish_positions, has_icon=True)
                else:
                    tk.Label(content_frame, text="🌾", font=('Arial', int(cell_size * 0.35)), bg='#2a3a2a').pack(expand=True)
                    tk.Label(content_frame, text="ПУСТО", font=('Arial', small_font), bg='#2a3a2a', fg='gray').pack()
            
            else:
                tk.Label(content_frame, text="⬜", font=('Arial', int(cell_size * 0.35)), bg='#2a3a2a', fg='gray').pack(expand=True)
    
    def update_cell_sizes(self):
        """Обновляет размер ячеек при изменении размера окна"""
        if hasattr(self, 'fields_frame') and self.fields_frame.winfo_exists():
            self.update_display()

    def log_message(self, msg):
        self.log_text.config(state='normal')
        self.log_text.insert('1.0', f"📅 День {self.current_day}: {msg}\n")
        self.log_text.see('1.0')
        self.log_text.config(state='disabled')
        self.root.update()
    
    def show_message(self, title, msg, icon="info"):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg='#2a3a2a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        
        # Создаём фрейм
        main_frame = tk.Frame(dialog, bg='#2a3a2a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Заголовок
        tk.Label(main_frame, text=f"{icons.get(icon, '📢')} {title}", 
                font=('Arial', 16, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=(0, 15))
        
        # Текст сообщения
        msg_label = tk.Label(main_frame, text=msg, font=('Arial', 12), 
                            bg='#2a3a2a', fg='white', wraplength=400, justify='left')
        msg_label.pack(pady=(0, 20))
        
        # Кнопка OK
        tk.Button(main_frame, text="OK", command=dialog.destroy, 
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), 
                 padx=20, pady=8).pack()
        
        # ✅ Автоматическая подстройка размера
        dialog.update_idletasks()
        
        # Получаем ширину и высоту содержимого
        req_width = main_frame.winfo_reqwidth() + 40  # + отступы
        req_height = main_frame.winfo_reqheight() + 30  # + отступы
        
        # Ограничиваем размеры
        width = max(350, min(600, req_width))
        height = max(200, min(500, req_height))
        
        dialog.geometry(f"{width}x{height}")
        
        # Центрируем
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        self.apply_hover_effect_to_all_buttons(dialog)
    
    def check_bankruptcy(self):
        """Проверяет банкротство игроков. Игрок банкротится, если его капитал < 0"""
        active_players = [p for p in self.players if not p.is_bankrupt]
        
        for player in self.players:
            if not player.is_bankrupt:
                capital = player.total_capital
                # ✅ Если капитал меньше 0 - игрок банкрот
                if capital < 0:
                    player.is_bankrupt = True
                    # Показываем сообщение о банкротстве с суммой долга
                    debt = abs(capital)
                    debt_gold = debt // QUARTERS_PER_GOLD
                    debt_q = debt % QUARTERS_PER_GOLD
                    if debt_q > 0:
                        debt_str = f"{debt_gold}.{debt_q} зол."
                    else:
                        debt_str = f"{debt_gold} зол."
                    self.show_toast(f"💀 {player.name} обанкротился! Долг: {debt_str}", "💀", 5000)
                    self.log_message(f"💀 {player.name} обанкротился и выбыл из игры! Долг: {debt_str}")
                    self.sound.play('lose')
        
        active_players = [p for p in self.players if not p.is_bankrupt]
        
        if len(active_players) == 1 and self.game_active:
            winner = active_players[0]
            capital = winner.total_capital
            gold = capital // QUARTERS_PER_GOLD
            quarter = capital % QUARTERS_PER_GOLD
            
            is_record = self.records.check_and_update_record(winner)
            record_text = "\n\n🏆 НОВЫЙ РЕКОРД! 🏆" if is_record else ""
            
            self.end_game()
            return True
        return False
    
    def update_display(self):
        self.check_bankruptcy()
        
        # ✅ ПРОВЕРКА: существует ли fields_frame
        try:
            if not self.fields_frame.winfo_exists():
                return
        except (tk.TclError, AttributeError):
            return
        
        # ✅ Синхронизация позиций для всех игроков
        for player in self.players:
            self.sync_horse_positions(player)
        
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        
        for idx, player in enumerate(self.players):
            row = idx // 2
            col = idx % 2
            self.draw_player_farm(player, row, col)
        
        while self.current_player_idx < len(self.players) and self.players[self.current_player_idx].is_bankrupt:
            self.current_player_idx += 1
            if self.current_player_idx >= len(self.players):
                self.current_player_idx = 0
                self.next_day()
        
        if self.current_player_idx >= len(self.players):
            return
        
        player = self.players[self.current_player_idx]
        gold = player.gold_quarters // QUARTERS_PER_GOLD
        quarter = player.gold_quarters % QUARTERS_PER_GOLD
        capital = player.total_capital
        capital_gold = capital // QUARTERS_PER_GOLD
        capital_q = capital % QUARTERS_PER_GOLD
        
        weekday = WEEKDAYS[(self.current_day - 1) % 7]
        event = WEEKDAY_EVENTS.get(weekday, "")
        
        self.info_label.config(text=f"📅 ДЕНЬ {self.current_day} / {self.days_total}  |  📆 НЕДЕЛЯ {self.week_number}")
        self.weekday_label.config(text=f"📅 {weekday} | {event}")
        
        if not player.action_taken and not player.is_bot and self.game_active and not self.race_mode and not self.auction_mode:
            self.resources_label.config(text=f"👤 {player.name}  |  💰 {gold}.{quarter} зол.  |  💎 КАПИТАЛ: {capital_gold}.{capital_q} зол.")
            
            # ✅ ПРОВЕРКА РЕСУРСОВ В НАЧАЛЕ ХОДА (только для людей, не ботов)
            # Используем флаг для предотвращения повторного показа
            if not hasattr(self, '_warning_shown_this_turn'):
                self._warning_shown_this_turn = False
            
            if not self._warning_shown_this_turn:
                total_radish_need = sum(h.food_per_day for h in player.horses)
                total_water_need = sum(h.water_per_day for h in player.horses)
                
                if player.radishes < total_radish_need or player.water_buckets < total_water_need:
                    self.show_message("⚠️ ВНИМАНИЕ!", 
                                    f"У вас может не хватить ресурсов для кормления лошадей в конце дня!\n\n"
                                    f"Нужно редисок: {total_radish_need}, у вас: {player.radishes}\n"
                                    f"Нужно воды: {total_water_need}, у вас: {player.water_buckets}\n\n"
                                    f"Рекомендуем посетить рынок прямо сейчас!", "warning")
                if player.radishes < total_radish_need and player.water_buckets < total_water_need:
                    self.sound.play('nugno_bolshe_redisok_i_vodii')
                    
                elif player.radishes < total_radish_need:
                    self.sound.play('nugno_bolshe_redisok')
                    
                elif player.water_buckets < total_water_need:
                    self.sound.play('nugno_bolshe_vodii')

                    self._warning_shown_this_turn = True
        elif self.race_mode and not player.action_taken and not player.is_bot:
            self.resources_label.config(text=f"👤 {player.name}  |  💰 {gold}.{quarter} зол.  |  🏇 ВЫБЕРИТЕ: УЧАСТВОВАТЬ ИЛИ ПРОПУСТИТЬ")
        elif self.auction_mode and not player.action_taken:
            self.resources_label.config(text=f"👤 {player.name}  |  💰 {gold}.{quarter} зол.  |  🏪 ВЫБЕРИТЕ ДЕЙСТВИЕ НА АУКЦИОНЕ")
        else:
            self.resources_label.config(text=f"👤 {player.name}  |  ⚡ ДЕЙСТВИЕ СДЕЛАНО  |  💎 КАПИТАЛ: {capital_gold}.{capital_q} зол.")
        
        for i in range(2):
            self.fields_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.fields_frame.grid_columnconfigure(i, weight=1)
        
        self.update_horses_list()
        
        if player.is_bot and not player.action_taken and self.game_active and not player.is_bankrupt:
            self.root.after(500, self.bot_turn)
    
    def show_training_animation(self, horse, progress_gain):
        self.sound.play('train')
        
        dialog = tk.Toplevel(self.root)
        dialog.title("🏇 ТРЕНИРОВКА")
        dialog.geometry("500x500")
        dialog.configure(bg='#2a3a2a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(dialog, text=f"🏇 {horse.name} ТРЕНИРУЕТСЯ 🏇", font=('Arial', 18, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=20)
        
        result_frame = tk.Frame(dialog, bg='#3a4a3a', relief='ridge', bd=3)
        result_frame.pack(pady=15, padx=30, fill='x')
        
        tk.Label(result_frame, text=f"Результат тренировки:", font=('Arial', 14),
                bg='#3a4a3a', fg='white').pack(pady=5)
        tk.Label(result_frame, text=f"+{progress_gain} к прогрессу!", font=('Arial', 20, 'bold'),
                bg='#3a4a3a', fg='#FFD700').pack(pady=5)
        
        # Показываем текущий прогресс и белые прокачки
        progress_percent = int((horse.training_progress / TRAINING_CIRCLE_MAX) * 100)
        tk.Label(result_frame, text=f"Текущий прогресс: {progress_percent}%", font=('Arial', 12),
                bg='#3a4a3a', fg='#90EE90').pack(pady=5)
        
        if horse.pending_upgrades > 0:
            tk.Label(result_frame, text=f"🏆 Доступно белых прокачек: {horse.pending_upgrades}", font=('Arial', 12, 'bold'),
                    bg='#3a4a3a', fg='#FFD700').pack(pady=5)
        
        if self.horse_gif_frames:
            gif_label = tk.Label(dialog, bg='#2a3a2a')
            gif_label.pack(pady=10)
            
            def animate_gif(frame=0):
                if frame < len(self.horse_gif_frames):
                    gif_label.config(image=self.horse_gif_frames[frame])
                    dialog.after(50, lambda: animate_gif(frame + 1))
                else:
                    animate_gif(0)
            
            animate_gif(0)
        else:
            horse_label = tk.Label(dialog, text=horse.icon, font=('Arial', 48), bg='#2a3a2a')
            horse_label.pack(pady=20)
            
            def animate_text(step=0):
                if step < 10:
                    horse_label.config(text="🏃 " + horse.icon)
                    dialog.update()
                    dialog.after(100, lambda: animate_text(step + 1))
                elif step < 20:
                    horse_label.config(text=horse.icon + " 🏃")
                    dialog.update()
                    dialog.after(100, lambda: animate_text(step + 1))
                else:
                    horse_label.config(text=horse.icon)
            
            animate_text()
        
        progress_bar = ttk.Progressbar(dialog, length=400, mode='determinate')
        progress_bar.pack(pady=20)
        
        step = 0

        def animate_progress():
            nonlocal step
            if step <= 100:
                progress_bar['value'] = step
                dialog.update()
                step += 2
                dialog.after(20, animate_progress)
            else:
                dialog.after(1500, dialog.destroy)
        
        animate_progress()
    
    def train_action(self):
        if not self.game_active:
            return
        player = self.players[self.current_player_idx]
        if player.action_taken:
            self.show_message("Ошибка", "Вы уже сделали действие в этом ходу!", "warning")
            return
        
        if not player.horses:
            self.show_message("Ошибка", "Нет лошадей для тренировки!", "warning")
            return
        
        # ПРОВЕРКА: есть ли хотя бы одна лошадь, которую можно тренировать
        trainable_horses = []
        for horse in player.horses:
            total_upgrades = len(horse.upgrades) + horse.pending_upgrades
            if total_upgrades < TRAINING_UPGRADES_MAX:
                trainable_horses.append(horse)
        
        if not trainable_horses:
            self.show_message("Ошибка", "Все ваши лошади достигли максимального уровня прокачек (4/4)!", "warning")
            return
        
        # СОЗДАЁМ ДИАЛОГОВОЕ ОКНО СО СПИСКОМ ЛОШАДЕЙ
        dialog = tk.Toplevel(self.root)
        dialog.title("🏇 ТРЕНИРОВКА")
        dialog.geometry("900x550")
        dialog.configure(bg='#2a3a2a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="ВЫБЕРИТЕ ЛОШАДЬ ДЛЯ ТРЕНИРОВКИ:", font=('Arial', 14, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        # Canvas и Scrollbar для прокрутки списка
        canvas = tk.Canvas(dialog, bg='#2a3a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a3a2a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # ФУНКЦИЯ ТРЕНИРОВКИ
        def do_training(horse_idx, dlg):
            horse = player.horses[horse_idx]
            
            # ПОВТОРНАЯ ПРОВЕРКА перед тренировкой
            total_upgrades = len(horse.upgrades) + horse.pending_upgrades
            if total_upgrades >= TRAINING_UPGRADES_MAX:
                self.show_message("Ошибка", f"{horse.name} уже достиг максимума прокачек (4/4)!", "warning")
                dlg.destroy()
                return
            
            dice = random.randint(1, 6)
            total = dice + horse.total_speed
            
            if total <= 0:
                self.log_message(f"🏇 {horse.name}: бросок {dice} + скорость {horse.total_speed} = {total} - Лошадь отказалась бежать!")
                self.show_toast(f"{horse.name} отказался тренироваться!", "😞", 4000)
                self.sound.play('train_fail')
            else:
                # Добавляем прогресс
                horse.training_progress += total
                self.log_message(f"🏇 {horse.name}: бросок {dice} + скорость {horse.total_speed} = {total}")
                
                # НЕМЕДЛЕННАЯ КОНВЕРТАЦИЯ
                gained_pending = 0
                while horse.training_progress >= TRAINING_CIRCLE_MAX:
                    if len(horse.upgrades) + horse.pending_upgrades >= TRAINING_UPGRADES_MAX:
                        # Достигнут максимум, не добавляем больше прокачек
                        horse.training_progress = TRAINING_CIRCLE_MAX - 1
                        break
                    horse.training_progress -= TRAINING_CIRCLE_MAX
                    horse.pending_upgrades += 1
                    gained_pending += 1
                
                if gained_pending > 0:
                    self.log_message(f"🎉 {horse.name}: получено {gained_pending} белых прокачек! Всего доступно: {horse.pending_upgrades}")
                    self.show_toast(f"{horse.name} получил {gained_pending} белую(ые) прокачку(и)!", "🎉", 5000)
                
                self.show_training_animation(horse, total)
            
            player.action_taken = True
            self.update_display()
            dlg.destroy()
        
        # ПЕРЕБИРАЕМ ВСЕХ ЛОШАДЕЙ ИГРОКА И СОЗДАЁМ КНОПКИ
        for i, horse in enumerate(player.horses):
            total_upgrades = len(horse.upgrades) + horse.pending_upgrades
            is_max = total_upgrades >= TRAINING_UPGRADES_MAX
            
            frame = tk.Frame(scrollable_frame, bg='#3a4a3a', relief='ridge', bd=2)
            frame.pack(fill='x', pady=5, padx=10)
            
            # Информация о лошади
            progress_percent = int((horse.training_progress / TRAINING_CIRCLE_MAX) * 100)
            
            info_frame = tk.Frame(frame, bg='#3a4a3a')
            info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)
            
            # Проверяем, является ли лошадь временной с заданием "train"
            task_mark = ""
            if horse.is_temp and player.temp_horse and player.temp_horse.horse.name == horse.name:
                if player.temp_horse.task_type == "train":
                    task_mark = " (ТРЕНИРОВКА)"
            
            max_mark = " [МАКСИМУМ]" if is_max else ""
            temp_mark = "🔵 (ОПЕКА) " if horse.is_temp else "🟤 "
            
            info_text = f"{temp_mark}{horse.icon} {horse.name}{task_mark} | Ур.{horse.level} | Ск.{horse.total_speed} | Прогресс: {progress_percent}%{max_mark} | "
            tk.Label(info_frame, text=info_text, font=('Arial', 11), 
                    bg='#3a4a3a', fg='white' if not is_max else '#FF8888').pack(side='left')
            
            # Отображаем прокачки
            upgrades_frame = self.create_upgrades_display(info_frame, horse, font_size=12, bg_color='#3a4a3a')
            upgrades_frame.pack(side='left')
            
            # Кнопка тренировки (отключаем если достигнут максимум)
            if is_max:
                btn = tk.Button(frame, text="МАКСИМУМ ДОСТИГНУТ", 
                               state='disabled',
                               bg='#555555', fg='gray', font=('Arial', 11, 'bold'), padx=20, pady=8)
            else:
                btn = tk.Button(frame, text="ТРЕНИРОВАТЬ", 
                               command=lambda idx=i, d=dialog: do_training(idx, d),
                               bg='#8B4513', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8)
            btn.pack(side='right', padx=10)
        
        self.apply_hover_effect_to_all_buttons(dialog)

    def lottery_action(self):
        if not self.game_active:
            return
        player = self.players[self.current_player_idx]
        if player.action_taken:
            self.show_message("Ошибка", "Вы уже сделали действие в этом ходу!", "warning")
            return
        
        max_tickets = min(4, player.gold_quarters // PRICE_RADISH)
        
        if max_tickets == 0:
            self.sound.play('nomoney')
            self.show_message("Ошибка", "Не хватает денег на билеты!", "error")
            return
        
        lottery_dialog = LotteryDialog(self.root, max_tickets, self.sound)
        self.root.wait_window(lottery_dialog)
        tickets = lottery_dialog.result
        
        if not tickets:
            return
        
        cost = tickets * PRICE_RADISH
        player.gold_quarters -= cost
        
        prizes = {1: 0, 2: 1, 3: 0, 4: 2, 5: 0, 6: QUARTERS_PER_GOLD}
        total_win = 0
        win_radish = 0
        win_water = 0
        
        results = []
        for _ in range(tickets):
            roll = random.randint(1, 6)
            if roll == 3:
                player.radishes += 1
                win_radish += 1
                results.append("🥕 Редиска")
            elif roll == 5:
                player.water_buckets += 1
                win_water += 1
                results.append("💧 Вода")
            else:
                win = prizes[roll]
                player.gold_quarters += win
                total_win += win
                if win > 0:
                    results.append(f"💰 {win} четверт.")
                else:
                    results.append("😞 Ничего")
        
        # Формируем результат для лога
        result_msg = f"Куплено {tickets} билетов: {', '.join(results)}"
        if total_win > 0:
            result_msg += f" | Выиграно: {total_win//QUARTERS_PER_GOLD}.{total_win%QUARTERS_PER_GOLD} зол."
        if win_radish > 0:
            result_msg += f" | +{win_radish} 🥕"
        if win_water > 0:
            result_msg += f" | +{win_water} 💧"
        
        self.log_message(f"🎰 ЛОТЕРЕЯ: {result_msg}")
        
        # Формируем результат для всплывающего сообщения
        toast_msg = f"Куплено {tickets} билетов\n"
        for r in results:
            toast_msg += f"{r}\n"
        if total_win > 0:
            toast_msg += f"💰 Выиграно: {total_win//QUARTERS_PER_GOLD}.{total_win%QUARTERS_PER_GOLD} зол."
        if win_radish > 0:
            toast_msg += f"\n🥕 +{win_radish} редисок"
        if win_water > 0:
            toast_msg += f"\n💧 +{win_water} воды"
        
        if total_win > 0 or win_radish > 0 or win_water > 0:
            self.sound.play('lucky')
            self.show_toast(toast_msg, "🎰", 5000)
        else:
            self.sound.play('unlucky')
            self.show_toast("Ничего не выиграно", "😞", 5000)
        
        player.action_taken = True
        self.update_display()
    
    def plant_radishes_action(self):
        if not self.game_active:
            return
        player = self.players[self.current_player_idx]
        
        if (self.current_day - 1) % 7 != 0:
            self.show_message("Ошибка", "Сажать редиски можно только в начале недели (в понедельник)!", "warning")
            return
        
        if player.action_taken:
            self.show_message("Ошибка", "Вы уже сделали действие в этом ходу!", "warning")
            return
        
        if player.fields == 0:
            self.show_message("Ошибка", "Нет полей для посадки! Купите поле на рынке.", "warning")
            return
        
        if player.radishes == 0:
            self.show_message("Ошибка", "Нет редисок для посадки! Купите редиски на рынке.", "warning")
            return
        
        if player.water_buckets == 0:
            self.show_message("Ошибка", "Нет воды для посадки! Купите воду на рынке.", "warning")
            return
        
        free_fields = player.get_free_fields()
        if not free_fields:
            self.show_message("Ошибка", "Нет свободных полей для посадки!", "warning")
            return
        
        # Рассчитываем максимальное количество редисок для посадки
        total_free_slots = 0
        for field_pos in free_fields:
            current_radishes = len(player.radish_positions.get(field_pos, []))
            total_free_slots += (RADISH_PER_FIELD - current_radishes)
        
        max_plant = min(total_free_slots, player.radishes, player.water_buckets)
        
        if max_plant <= 0:
            self.show_message("Ошибка", "Нет места для посадки редисок!", "warning")
            return
        
        # Диалог выбора количества редисок для посадки
        plant_dialog = tk.Toplevel(self.root)
        plant_dialog.title("🌱 ПОСАДКА РЕДИСОК")
        plant_dialog.geometry("400x350")
        plant_dialog.configure(bg='#2a3a2a')
        plant_dialog.transient(self.root)
        plant_dialog.grab_set()
        
        tk.Label(plant_dialog, text="🌱 ПОСАДКА РЕДИСОК 🌱", font=('Arial', 16, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        tk.Label(plant_dialog, text=f"🥕 Редисок: {player.radishes} | 💧 Воды: {player.water_buckets}", 
                font=('Arial', 12), bg='#2a3a2a', fg='white').pack(pady=5)
        
        tk.Label(plant_dialog, text=f"Свободно места на полях: {total_free_slots} (макс. 4 на поле)", 
                font=('Arial', 12), bg='#2a3a2a', fg='#90EE90').pack(pady=5)
        
        tk.Label(plant_dialog, text="Выберите количество редисок для посадки:", 
                font=('Arial', 12), bg='#2a3a2a', fg='white').pack(pady=10)
        
        plant_var = tk.IntVar(value=min(4, max_plant))
        plant_spinbox = tk.Spinbox(plant_dialog, from_=1, to=max_plant, textvariable=plant_var,
                                    width=10, font=('Arial', 14))
        plant_spinbox.pack(pady=10)
        
        def do_auto_plant():
            count = plant_var.get()
            if count <= 0:
                plant_dialog.destroy()
                return
            
            # Автоматическое распределение редисок по полям
            remaining = count
            fields_to_plant = free_fields.copy()
            
            for field_pos in fields_to_plant:
                if remaining <= 0:
                    break
                current_radishes = len(player.radish_positions.get(field_pos, []))
                free_slots = RADISH_PER_FIELD - current_radishes
                if free_slots > 0:
                    to_plant = min(remaining, free_slots)
                    planted = player.plant_radishes(field_pos, to_plant)
                    remaining -= planted
            
            planted_count = count - remaining
            if planted_count > 0:
                self.log_message(f"🌱 {player.name} посадил {planted_count} редисок на {len(fields_to_plant)} полях")
                self.show_toast(f"Посажено {planted_count} редисок! Потрачено {planted_count} воды.", "🌱", 4000)
                player.action_taken = True
                self.update_display()
            
            plant_dialog.destroy()
        
        btn_frame = tk.Frame(plant_dialog, bg='#2a3a2a')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="ПОСАДИТЬ", command=do_auto_plant,
                 bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=5).pack(side='left', padx=15)
        
        tk.Button(btn_frame, text="ОТМЕНА", command=plant_dialog.destroy,
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=5).pack(side='left', padx=15)
    
    def resurrect_horse_to_farmer(self, horse_name, level, was_temp=False):
        """Воскрешает умершую лошадь у случайного фермера (без прокачек)"""
        # Находим фермера с наименьшим количеством лошадей
        min_horses = float('inf')
        target_owner = None
        
        for owner in self.horse_owners.values():
            total_horses = len(owner.horses) + len(owner.horses_for_sale)
            if total_horses < min_horses:
                min_horses = total_horses
                target_owner = owner
        
        if target_owner is None:
            target_owner = random.choice(list(self.horse_owners.values()))
        
        # Создаём новую лошадь БЕЗ прокачек
        new_horse = Horse(level, horse_name, target_owner.color, False)
        new_horse.upgrades = []
        new_horse.upgrade_count = 0
        new_horse.training_progress = 0
        new_horse.pending_upgrades = 0
        
        # Добавляем фермеру в табун (НЕ на продажу)
        target_owner.horses.append(new_horse)
        
        if was_temp:
            self.log_message(f"🌱 Временная лошадь {horse_name} (Ур.{level}) воскрешена у фермера {target_owner.name}")
        else:
            self.log_message(f"🌱 {horse_name} (Ур.{level}) воскрешена у фермера {target_owner.name}")
        
        # НЕ вызываем update_market_horses() здесь,
        # чтобы лошадь не выставлялась на продажу автоматически
        # Она попадёт на рынок только когда освободится место

    def close_all_windows(self):
        """Закрывает все побочные окна (диалоги, меню, оверлеи)"""
        # Закрываем меню
        if hasattr(self, 'menu_window') and self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.destroy()
            self.menu_window = None
        
        # Закрываем оверлей
        if hasattr(self, 'event_overlay') and self.event_overlay and self.event_overlay.winfo_exists():
            self.event_overlay.destroy()
            self.event_overlay = None
        
        # Закрываем окно аукциона
        if hasattr(self, 'auction_window') and self.auction_window and self.auction_window.winfo_exists():
            self.auction_window.destroy()
            self.auction_window = None
        
        # Закрываем все дочерние окна Toplevel
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                try:
                    # Проверяем, что это не главное окно
                    if widget != self.root:
                        widget.destroy()
                except:
                    pass

    def buy_horse_from_owner(self, owner, horse, player, dialog):
        """Покупает лошадь у фермера (с сохранением всех прокачек)"""
        # ИСПОЛЬЗУЕМ sell_price() ДЛЯ РАСЧЁТА ЦЕНЫ
        price = horse.sell_price()
        
        # Проверяем, хватает ли денег (но не запрещаем уходить в минус, если после покупки капитал станет отрицательным)
        if player.gold_quarters < price:
            self.sound.play('nomoney')
            self.show_message("Ошибка", f"Не хватает денег! Нужно {price//QUARTERS_PER_GOLD}.{price%QUARTERS_PER_GOLD} зол.", "error")
            return
        
        free_stable = player.get_free_stable()
        if free_stable == -1:
            self.show_message("Ошибка", "Нет свободных стойл! Постройте новое стойло.", "error")
            return
        
        # СОХРАНЯЕМ ВСЕ ХАРАКТЕРИСТИКИ ЛОШАДИ
        new_horse = Horse(horse.level, horse.name, player.color, False)
        new_horse.upgrades = horse.upgrades.copy()
        new_horse.upgrade_count = len(new_horse.upgrades)
        new_horse.training_progress = horse.training_progress
        new_horse.pending_upgrades = horse.pending_upgrades
        
        # Списываем деньги (игрок может уйти в минус, если его капитал позволял покупку)
        player.gold_quarters -= price
        owner.money += price
        
        # Удаляем из списка продажи
        if horse in owner.horses_for_sale:
            owner.horses_for_sale.remove(horse)
        
        # Удаляем из списка лошадей фермера
        if horse in owner.horses:
            owner.horses.remove(horse)
        
        # Добавляем игроку
        player.horse_positions[free_stable] = len(player.horses)
        player.horses.append(new_horse)
        
        # ✅ НЕ ВЫЗЫВАЕМ update_market_horses() здесь - мы уже удалили лошадь вручную
        
        # ЗВУК ПОКУПКИ
        self.sound.play('buy')
        
        # Форматируем цену для вывода
        price_gold = price // QUARTERS_PER_GOLD
        price_q = price % QUARTERS_PER_GOLD
        if price_q > 0:
            price_str = f"{price_gold}.{price_q} зол."
        else:
            price_str = f"{price_gold} зол."
        
        self.log_message(f"🛒 {player.name} купил лошадь {horse.name} у {owner.name} за {price_str} (прокачек: {len(new_horse.upgrades)})")
        self.show_toast(f"Куплена лошадь {horse.name} с {len(new_horse.upgrades)} прокачками!", "🛒", 4000)
        
        # ✅ Проверяем банкротство после покупки
        self.check_bankruptcy()
        
        dialog.destroy()
        self.update_display()

    def sell_horse_to_farmer(self, horse, pos, player, dialog):
        """Продаёт лошадь фермеру (лошадь появляется на рынке с сохранением прокачек)"""
        # ПРАВИЛЬНАЯ ЦЕНА с учётом прокачек
        price = horse.sell_price()  # sell_price уже учитывает прокачки!
        
        # Находим фермера, который может купить (с достаточным количеством денег)
        available_owners = []
        for owner in self.horse_owners.values():
            if owner.money >= price:
                available_owners.append(owner)
        
        if not available_owners:
            self.show_message("Ошибка", "Ни один фермер не может купить эту лошадь (недостаточно средств)!", "error")
            return
        
        # Выбираем случайного фермера из доступных
        owner = random.choice(available_owners)
        
        # ✅ ПРОВЕРЯЕМ: если эта лошадь была у фермера в списке продажи - удаляем её
        # (это может случиться, если лошадь была на рынке, игрок её купил, а потом продаёт обратно)
        for horse_in_sale in owner.horses_for_sale[:]:  # Создаём копию для безопасного удаления
            if horse_in_sale.name == horse.name:
                owner.horses_for_sale.remove(horse_in_sale)
                self.log_message(f"🗑️ Лошадь {horse.name} удалена из списка продажи фермера {owner.name}")
                break
        
        # СОХРАНЯЕМ ВСЕ ХАРАКТЕРИСТИКИ ЛОШАДИ
        horse_for_sale = Horse(horse.level, horse.name, owner.color, False)
        horse_for_sale.upgrades = horse.upgrades.copy()
        horse_for_sale.upgrade_count = len(horse_for_sale.upgrades)
        horse_for_sale.training_progress = horse.training_progress
        horse_for_sale.pending_upgrades = horse.pending_upgrades
        
        # Добавляем фермеру
        owner.horses.append(horse_for_sale)
        owner.money -= price
        
        # Удаляем лошадь у игрока
        if pos in player.horse_positions:
            del player.horse_positions[pos]
        player.horses.remove(horse)
        player.gold_quarters += price
        
        # ✅ Выставляем на продажу (если есть место) - ТОЛЬКО если не достигнут лимит
        if len(owner.horses_for_sale) < owner.max_sale_horses:
            owner.horses_for_sale.append(horse_for_sale)
            self.log_message(f"📢 {horse.name} выставлена на продажу фермером {owner.name} за {price//QUARTERS_PER_GOLD}.{price%QUARTERS_PER_GOLD} зол. (прокачек: {len(horse_for_sale.upgrades)})")
        else:
            self.log_message(f"ℹ️ {horse.name} добавлена фермеру {owner.name}, но не выставлена на продажу (лимит {owner.max_sale_horses})")
        
        # ЗВУК ПРОДАЖИ
        self.sound.play('sell')

        self.log_message(f"💰 {player.name} продал лошадь {horse.name} фермеру {owner.name} за {price//QUARTERS_PER_GOLD}.{price%QUARTERS_PER_GOLD} зол.")
        self.show_toast(f"Лошадь {horse.name} продана! +{price//QUARTERS_PER_GOLD}.{price%QUARTERS_PER_GOLD} зол.", "💰", 4000)
        
        # ✅ НЕ ВЫЗЫВАЕМ update_market_horses() здесь - мы уже добавили лошадь вручную
        # self.update_market_horses()  <-- УБРАТЬ
        
        dialog.destroy()
        self.update_display()

    def clear_market_horses(self):
        """Очищает всех лошадей на продажу перед новым аукционом"""
        for owner in self.horse_owners.values():
            owner.horses_for_sale = []  # Полностью очищаем список продажи

    def update_market_horses(self):
        """Обновляет список лошадей на продажу (всегда должно быть 4)"""
        # Считаем текущие лошади на продажу

        # ✅ ОЧИЩАЕМ РЫНОК ПЕРЕД ГЕНЕРАЦИЕЙ НОВЫХ ЗАДАНИЙ
        self.clear_market_horses()

        current_sale = []
        for owner in self.horse_owners.values():
            for horse in owner.horses_for_sale:
                current_sale.append((owner, horse))
        
        # Если уже 4 или больше - ничего не делаем
        if len(current_sale) >= 4:
            return
        
        # Сколько нужно добавить
        needed = 4 - len(current_sale)
        
        # Собираем всех лошадей фермеров, которые не на продаже
        available = []
        for owner in self.horse_owners.values():
            for horse in owner.horses:
                # ✅ Проверяем, что лошадь не на продаже И ещё не добавлена
                if horse not in owner.horses_for_sale and (owner, horse) not in available:
                    available.append((owner, horse))
        
        # Перемешиваем для случайности
        random.shuffle(available)
        
        added = 0
        for owner, horse in available:
            if added >= needed:
                break
            # Проверяем лимит продажи у фермера
            if len(owner.horses_for_sale) < owner.max_sale_horses:
                # ✅ ДВАЖДЫ ПРОВЕРЯЕМ, что лошадь ещё не добавлена
                if horse not in owner.horses_for_sale:
                    owner.horses_for_sale.append(horse)
                    added += 1
                    # Не пишем в лог, т.к. это может вызвать проблемы при загрузке

    def market_action(self):
        if not self.game_active:
            return
        player = self.players[self.current_player_idx]
        if player.action_taken and not self.auction_mode:
            self.show_message("Ошибка", "Вы уже сделали действие в этом ходу!", "warning")
            return
        
        is_auction_day = (self.current_day % 7 == 0)
        is_auction_mode = self.auction_mode
        
        dialog = tk.Toplevel(self.root)
        dialog.title("🏪 РЫНОК")
        dialog.geometry("880x800")
        dialog.configure(bg='#2a3a2a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="🏪 ДОБРО ПОЖАЛОВАТЬ НА РЫНОК 🏪", font=('Arial', 16, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        gold = player.gold_quarters // QUARTERS_PER_GOLD
        quarter = player.gold_quarters % QUARTERS_PER_GOLD
        tk.Label(dialog, text=f"👤 {player.name}  |  💰 {gold}.{quarter} зол.  |  🥕 {player.radishes}  |  💧 {player.water_buckets}", 
                font=('Arial', 13, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=8)
        
        if not is_auction_day and not is_auction_mode:
            warning_frame = tk.Frame(dialog, bg='#8B4513', relief='ridge', bd=2)
            warning_frame.pack(fill='x', padx=20, pady=10)
            tk.Label(warning_frame, text="⚠️ СТРОЙКИ, ЛОШАДИ, ПРОКАЧКИ И ЗАДАНИЯ ДОСТУПНЫ ТОЛЬКО В ВОСКРЕСЕНЬЕ ИЛИ НА АУКЦИОНЕ ⚠️", 
                    font=('Arial', 11, 'bold'), bg='#8B4513', fg='#FFD700').pack(pady=8)
        
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # ==================== ВКЛАДКА ПОКУПКА ====================
        buy_frame = tk.Frame(notebook, bg='#2a3a2a')
        notebook.add(buy_frame, text="🛒 ПОКУПКА")
        
        buy_items_frame = tk.Frame(buy_frame, bg='#2a3a2a')
        buy_items_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        if is_auction_day or is_auction_mode:
            tk.Label(buy_items_frame, text="🏗️ ПОСТРОЙКИ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(anchor='w', pady=(10,0))
            
            stable_frame = tk.Frame(buy_items_frame, bg='#2a3a2a')
            stable_frame.pack(fill='x', pady=5)
            tk.Label(stable_frame, text="🏠 СТОЙЛО (1 золотая/шт):", font=('Arial', 11),
                    bg='#2a3a2a', fg='white').pack(side='left')
            stable_buy_spinbox = tk.Spinbox(stable_frame, from_=0, to=10, width=8, font=('Arial', 11))
            stable_buy_spinbox.delete(0, tk.END)
            stable_buy_spinbox.insert(0, "0")
            stable_buy_spinbox.pack(side='left', padx=10)
            
            field_frame = tk.Frame(buy_items_frame, bg='#2a3a2a')
            field_frame.pack(fill='x', pady=5)
            tk.Label(field_frame, text="🌾 ПОЛЕ (1 золотая/шт):", font=('Arial', 11),
                    bg='#2a3a2a', fg='white').pack(side='left')
            field_buy_spinbox = tk.Spinbox(field_frame, from_=0, to=10, width=8, font=('Arial', 11))
            field_buy_spinbox.delete(0, tk.END)
            field_buy_spinbox.insert(0, "0")
            field_buy_spinbox.pack(side='left', padx=10)

            # ЛОШАДИ НА ПРОДАЖУ С ПРОКРУТКОЙ
            tk.Label(buy_items_frame, text="\n🐴 ЛОШАДИ НА ПРОДАЖУ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(anchor='w', pady=(20,5))

            # Создаём фрейм для Canvas с прокруткой
            horses_buy_frame = tk.Frame(buy_items_frame, bg='#2a3a2a')
            horses_buy_frame.pack(fill='both', expand=True, pady=5)

            # Создаём Canvas и Scrollbar
            buy_canvas = tk.Canvas(horses_buy_frame, bg='#2a3a2a', highlightthickness=0, height=200)
            buy_scrollbar = tk.Scrollbar(horses_buy_frame, orient="vertical", command=buy_canvas.yview)
            buy_scrollable_frame = tk.Frame(buy_canvas, bg='#2a3a2a')

            buy_scrollable_frame.bind(
                "<Configure>",
                lambda e: buy_canvas.configure(scrollregion=buy_canvas.bbox("all"))
            )

            buy_canvas.create_window((0, 0), window=buy_scrollable_frame, anchor="nw")
            buy_canvas.configure(yscrollcommand=buy_scrollbar.set)

            # Упаковываем
            buy_canvas.pack(side="left", fill="both", expand=True)
            buy_scrollbar.pack(side="right", fill="y")

            def on_buy_mousewheel(event):
                buy_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            buy_canvas.bind("<Enter>", lambda e: buy_canvas.bind_all("<MouseWheel>", on_buy_mousewheel))
            buy_canvas.bind("<Leave>", lambda e: buy_canvas.unbind_all("<MouseWheel>"))

            # Собираем лошадей на продажу от всех владельцев
            horses_for_sale = []
            for owner in self.horse_owners.values():
                for horse in owner.horses_for_sale:
                    horses_for_sale.append((owner, horse))

            if horses_for_sale:
                for owner, horse in horses_for_sale:
                    frame = tk.Frame(buy_scrollable_frame, bg='#3a4a3a', relief='ridge', bd=2)
                    frame.pack(fill='x', pady=5, padx=10)
                    
                    price = horse.sell_price()
                    price_gold = price // QUARTERS_PER_GOLD
                    price_q = price % QUARTERS_PER_GOLD
                    
                    info_text = f"{horse.icon} {horse.name} (Ур.{horse.level}) - {price_gold}.{price_q} зол. | Владелец: {owner.name}"
                    tk.Label(frame, text=info_text, font=('Arial', 11), 
                            bg='#3a4a3a', fg='white').pack(side='left', padx=15, pady=10)
                    
                    upgrades_frame = self.create_upgrades_display(frame, horse, font_size=10, bg_color='#3a4a3a')
                    upgrades_frame.pack(side='left', padx=10)
                    
                    tk.Button(frame, text="КУПИТЬ", 
                             command=lambda o=owner, h=horse, d=dialog: self.buy_horse_from_owner(o, h, player, d),
                             bg='#4a7a2e', fg='white', font=('Arial', 11, 'bold'), padx=15).pack(side='right', padx=15)
            else:
                tk.Label(buy_scrollable_frame, text="  Нет лошадей на продажу", 
                        font=('Arial', 10), bg='#2a3a2a', fg='gray').pack(anchor='w', pady=5)

        else:
            stable_buy_spinbox = None
            field_buy_spinbox = None
            tk.Label(buy_items_frame, text="⚠️ СТРОЙКИ МОЖНО ПОКУПАТЬ ТОЛЬКО В ВОСКРЕСЕНЬЕ", 
                    font=('Arial', 11, 'bold'), bg='#2a3a2a', fg='#FF4444').pack(anchor='w', pady=10)
        
        tk.Label(buy_items_frame, text="\n🥕 РЕСУРСЫ:", 
                font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(anchor='w', pady=(20,0))
        
        radish_frame = tk.Frame(buy_items_frame, bg='#2a3a2a')
        radish_frame.pack(fill='x', pady=5)
        tk.Label(radish_frame, text="🥕 РЕДИСКИ (1 четвертак/шт):", font=('Arial', 11),
                bg='#2a3a2a', fg='white').pack(side='left')
        radish_buy_spinbox = tk.Spinbox(radish_frame, from_=0, to=100, width=8, font=('Arial', 11))
        radish_buy_spinbox.delete(0, tk.END)
        radish_buy_spinbox.insert(0, "0")
        radish_buy_spinbox.pack(side='left', padx=10)
        
        water_frame = tk.Frame(buy_items_frame, bg='#2a3a2a')
        water_frame.pack(fill='x', pady=5)
        tk.Label(water_frame, text="💧 ВОДА (1 четвертак/шт):", font=('Arial', 11),
                bg='#2a3a2a', fg='white').pack(side='left')
        water_buy_spinbox = tk.Spinbox(water_frame, from_=0, to=100, width=8, font=('Arial', 11))
        water_buy_spinbox.delete(0, tk.END)
        water_buy_spinbox.insert(0, "0")
        water_buy_spinbox.pack(side='left', padx=10)
        
        # ==================== ВКЛАДКА ПРОДАЖА ====================
        sell_frame = tk.Frame(notebook, bg='#2a3a2a')
        notebook.add(sell_frame, text="💰 ПРОДАЖА")
        
        # ⚠️ ВАЖНО: ЭТО ГЛАВНЫЙ sell_items_frame ДЛЯ ВСЕЙ ВКЛАДКИ ПРОДАЖА
        sell_items_frame = tk.Frame(sell_frame, bg='#2a3a2a')
        sell_items_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(sell_items_frame, text="🥕 РЕСУРСЫ:", 
                font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(anchor='w', pady=(10,0))
        
        sell_radish_frame = tk.Frame(sell_items_frame, bg='#2a3a2a')
        sell_radish_frame.pack(fill='x', pady=5)
        tk.Label(sell_radish_frame, text="🥕 ПРОДАТЬ РЕДИСКИ (1 четвертак/шт):", font=('Arial', 11),
                bg='#2a3a2a', fg='white').pack(side='left')
        radish_sell_spinbox = tk.Spinbox(sell_radish_frame, from_=0, to=100, width=8, font=('Arial', 11))
        radish_sell_spinbox.delete(0, tk.END)
        radish_sell_spinbox.insert(0, "0")
        radish_sell_spinbox.pack(side='left', padx=10)
        
        sell_water_frame = tk.Frame(sell_items_frame, bg='#2a3a2a')
        sell_water_frame.pack(fill='x', pady=5)
        tk.Label(sell_water_frame, text="💧 ПРОДАТЬ ВОДУ (1 четвертак/шт):", font=('Arial', 11),
                bg='#2a3a2a', fg='white').pack(side='left')
        water_sell_spinbox = tk.Spinbox(sell_water_frame, from_=0, to=100, width=8, font=('Arial', 11))
        water_sell_spinbox.delete(0, tk.END)
        water_sell_spinbox.insert(0, "0")
        water_sell_spinbox.pack(side='left', padx=10)
        
        if is_auction_day or is_auction_mode:
            tk.Label(sell_items_frame, text="\n🏗️ ПРОДАЖА ПОСТРОЕК:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(anchor='w', pady=(20,10))
            
            empty_stables = [i for i in range(MAX_LAND) if player.land_map[i] == 1 and i not in player.horse_positions]
            if empty_stables:
                stable_var = tk.IntVar()
                stable_var.set(empty_stables[0])
                stable_menu = tk.OptionMenu(sell_items_frame, stable_var, *empty_stables)
                stable_menu.config(bg='#3a4a3a', fg='white', width=20)
                stable_menu.pack(anchor='w', pady=5)
                tk.Button(sell_items_frame, text="🏠 ПРОДАТЬ ВЫБРАННОЕ СТОЙЛО (1 золотая)", 
                         command=lambda: self.sell_stable(stable_var.get(), player, dialog),
                         bg='#8B4513', fg='white', font=('Arial', 11)).pack(anchor='w', pady=5)
            
            empty_fields = [i for i in range(MAX_LAND) if player.land_map[i] == 2 and i not in player.radish_positions]
            if empty_fields:
                field_var = tk.IntVar()
                field_var.set(empty_fields[0])
                field_menu = tk.OptionMenu(sell_items_frame, field_var, *empty_fields)
                field_menu.config(bg='#3a4a3a', fg='white', width=20)
                field_menu.pack(anchor='w', pady=5)
                tk.Button(sell_items_frame, text="🌾 ПРОДАТЬ ВЫБРАННОЕ ПОЛЕ (1 золотая)", 
                         command=lambda: self.sell_field(field_var.get(), player, dialog),
                         bg='#8B4513', fg='white', font=('Arial', 11)).pack(anchor='w', pady=5)

            # ПРОДАЖА ЛОШАДИ ФЕРМЕРУ С ПРОКРУТКОЙ
            tk.Label(sell_items_frame, text="\n🐴 ПРОДАЖА ЛОШАДИ ФЕРМЕРУ:", 
                    font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(anchor='w', pady=(20,5))

            # Создаём фрейм для Canvas с прокруткой
            horses_sell_frame = tk.Frame(sell_items_frame, bg='#2a3a2a')
            horses_sell_frame.pack(fill='both', expand=True, pady=5)

            # Создаём Canvas и Scrollbar
            sell_canvas = tk.Canvas(horses_sell_frame, bg='#2a3a2a', highlightthickness=0, height=200)
            sell_scrollbar = tk.Scrollbar(horses_sell_frame, orient="vertical", command=sell_canvas.yview)
            sell_scrollable_frame = tk.Frame(sell_canvas, bg='#2a3a2a')

            sell_scrollable_frame.bind(
                "<Configure>",
                lambda e: sell_canvas.configure(scrollregion=sell_canvas.bbox("all"))
            )

            sell_canvas.create_window((0, 0), window=sell_scrollable_frame, anchor="nw")
            sell_canvas.configure(yscrollcommand=sell_scrollbar.set)

            # Упаковываем
            sell_canvas.pack(side="left", fill="both", expand=True)
            sell_scrollbar.pack(side="right", fill="y")

            def on_sell_mousewheel(event):
                sell_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            sell_canvas.bind("<Enter>", lambda e: sell_canvas.bind_all("<MouseWheel>", on_sell_mousewheel))
            sell_canvas.bind("<Leave>", lambda e: sell_canvas.unbind_all("<MouseWheel>"))

            # Свои лошади (не временные) - С ПРОВЕРКОЙ ИНДЕКСОВ
            own_horses_for_sale = []
            positions_to_remove = []
            for pos, horse_idx in list(player.horse_positions.items()):
                if horse_idx < len(player.horses):
                    horse = player.horses[horse_idx]
                    if not horse.is_temp:
                        own_horses_for_sale.append((pos, horse))
                else:
                    positions_to_remove.append(pos)

            # Удаляем некорректные позиции
            for pos in positions_to_remove:
                del player.horse_positions[pos]
                self.log_message(f"⚠️ Исправлена ошибка: удалена позиция {pos} с несуществующей лошадью")

            if own_horses_for_sale:
                for pos, horse in own_horses_for_sale:
                    frame = tk.Frame(sell_scrollable_frame, bg='#3a4a3a', relief='ridge', bd=2)
                    frame.pack(fill='x', pady=5, padx=10)
                    
                    price = horse.sell_price()
                    price_gold = price // QUARTERS_PER_GOLD
                    price_q = price % QUARTERS_PER_GOLD
                    
                    info_text = f"{horse.icon} {horse.name} (Ур.{horse.level}) - {price_gold}.{price_q} зол."
                    tk.Label(frame, text=info_text, font=('Arial', 11), 
                            bg='#3a4a3a', fg='white').pack(side='left', padx=15, pady=10)
                    
                    upgrades_frame = self.create_upgrades_display(frame, horse, font_size=10, bg_color='#3a4a3a')
                    upgrades_frame.pack(side='left', padx=10)
                    
                    tk.Button(frame, text="ПРОДАТЬ ФЕРМЕРУ", 
                             command=lambda h=horse, p=pos, d=dialog: self.sell_horse_to_farmer(h, p, player, d),
                             bg='#8B4513', fg='white', font=('Arial', 11, 'bold'), padx=15).pack(side='right', padx=15)
            else:
                tk.Label(sell_scrollable_frame, text="  Нет своих лошадей для продажи", 
                        font=('Arial', 10), bg='#2a3a2a', fg='gray').pack(anchor='w', pady=5)
        
        # ==================== ВКЛАДКА ПРОКАЧКИ ====================
        if is_auction_day or is_auction_mode:
            upgrade_frame = tk.Frame(notebook, bg='#2a3a2a')
            notebook.add(upgrade_frame, text="⚡ ПРОКАЧКИ")
            
            upgrade_items_frame = tk.Frame(upgrade_frame, bg='#2a3a2a')
            upgrade_items_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            tk.Label(upgrade_items_frame, text="КУПИТЬ ПРОКАЧКИ ДЛЯ ЛОШАДЕЙ", 
                    font=('Arial', 14, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=10)
            
            for horse in player.horses:
                if horse.pending_upgrades > 0:
                    frame = tk.Frame(upgrade_items_frame, bg='#3a4a3a', relief='ridge', bd=2)
                    frame.pack(fill='x', pady=8, padx=10)
                    
                    info = f"{horse.icon} {horse.name} (Ур.{horse.level}) - Доступно белых прокачек: {horse.pending_upgrades}"
                    tk.Label(frame, text=info, font=('Arial', 12), bg='#3a4a3a', fg='white').pack(side='left', padx=15, pady=10)
                    
                    btn = tk.Button(frame, text="КУПИТЬ ПРОКАЧКУ (1 четвертак)", 
                                   command=lambda h=horse, d=dialog: self.buy_pending_upgrade(h, player, d),
                                   bg='#4a7a2e', fg='white', font=('Arial', 11, 'bold'), padx=15)
                    btn.pack(side='right', padx=15)
                else:
                    frame = tk.Frame(upgrade_items_frame, bg='#3a4a3a', relief='ridge', bd=2)
                    frame.pack(fill='x', pady=5, padx=10)
                    tk.Label(frame, text=f"{horse.icon} {horse.name} - Нет доступных прокачек", 
                            font=('Arial', 11), bg='#3a4a3a', fg='gray').pack(pady=10)
        
        # ==================== ВКЛАДКА ЗАДАНИЯ ====================
        if is_auction_day or is_auction_mode:
            tasks_frame = tk.Frame(notebook, bg='#2a3a2a')
            notebook.add(tasks_frame, text="📋 ЗАДАНИЯ")
            
            tasks_items_frame = tk.Frame(tasks_frame, bg='#2a3a2a')
            tasks_items_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            tk.Label(tasks_items_frame, text="ВЗЯТЬ ЛОШАДЬ НА ПОПЕЧЕНИЕ", 
                    font=('Arial', 14, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=10)
            
            free_stable = player.get_free_stable()
            if free_stable != -1:
                task_btn = tk.Button(tasks_items_frame, text="ПОСМОТРЕТЬ ДОСТУПНЫЕ ЗАДАНИЯ", 
                                    command=lambda: self.show_available_tasks(player, dialog),
                                    bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10)
                task_btn.pack(pady=20)
                tk.Label(tasks_items_frame, text="Вы получите аванс и задание на неделю", 
                        font=('Arial', 10), bg='#2a3a2a', fg='#90EE90').pack()
                tk.Label(tasks_items_frame, text="За выполнение получите награду", 
                        font=('Arial', 10), bg='#2a3a2a', fg='#90EE90').pack()
            else:
                tk.Label(tasks_items_frame, text="❌ Нет свободных стойл для опеки", 
                        font=('Arial', 12, 'bold'), bg='#2a3a2a', fg='#FF4444').pack(pady=20)
        
        # ==================== КНОПКИ ВНИЗУ ====================
        def execute_buy():
            stables = int(stable_buy_spinbox.get()) if stable_buy_spinbox else 0
            fields = int(field_buy_spinbox.get()) if field_buy_spinbox else 0
            radishes = int(radish_buy_spinbox.get()) if radish_buy_spinbox.get().isdigit() else 0
            water = int(water_buy_spinbox.get()) if water_buy_spinbox.get().isdigit() else 0
            
            total_cost = (stables * PRICE_STABLE) + (fields * PRICE_FIELD) + (radishes * PRICE_RADISH) + (water * PRICE_WATER)
            
            if total_cost == 0:
                self.show_message("Ошибка", "Введите количество хотя бы одного товара!", "warning")
                return
            
            if (stables > 0 or fields > 0) and not (is_auction_day or is_auction_mode):
                self.show_message("Ошибка", "Стойла и поля можно покупать только в воскресенье!", "warning")
                return
            
            if player.gold_quarters >= total_cost:
                bought_items = []
                
                if stables > 0:
                    added = player.add_stable(stables)
                    if added > 0:
                        player.gold_quarters -= added * PRICE_STABLE
                        bought_items.append(f"{added} стойл")
                        self.sound.play('buy')
                    else:
                        self.show_message("Ошибка", "Нет свободной земли для стойл!", "error")
                        return
                
                if fields > 0:
                    added = player.add_field(fields)
                    if added > 0:
                        player.gold_quarters -= added * PRICE_FIELD
                        bought_items.append(f"{added} полей")
                        self.sound.play('buy')
                    else:
                        self.show_message("Ошибка", "Нет свободной земли для полей!", "error")
                        return
                
                if radishes > 0:
                    player.gold_quarters -= radishes * PRICE_RADISH
                    player.radishes += radishes
                    bought_items.append(f"{radishes} редисок")
                    self.sound.play('buy')
                
                if water > 0:
                    player.gold_quarters -= water * PRICE_WATER
                    player.water_buckets += water
                    bought_items.append(f"{water} воды")
                    self.sound.play('buy')
                
                if bought_items:
                    items_text = ", ".join(bought_items)
                    self.log_message(f"🛒 {player.name} купил: {items_text}")
                    self.show_toast(f"Куплено: {items_text}", "🛒", 5000)
                
                if not self.auction_mode:
                    player.action_taken = True
                self.update_display()
                dialog.destroy()
            else:
                self.sound.play('nomoney')
                self.show_message("Ошибка", "Не хватает денег!", "error")
        
        def execute_sell():
            sold_items = []
            
            radishes = int(radish_sell_spinbox.get()) if radish_sell_spinbox.get().isdigit() else 0
            if radishes > 0:
                if radishes <= player.radishes:
                    player.radishes -= radishes
                    player.gold_quarters += radishes * PRICE_RADISH
                    sold_items.append(f"{radishes} редисок")
                    self.sound.play('sell')
                else:
                    self.show_message("Ошибка", f"Недостаточно редисок! У вас: {player.radishes}", "error")
                    return
            
            water = int(water_sell_spinbox.get()) if water_sell_spinbox.get().isdigit() else 0
            if water > 0:
                if water <= player.water_buckets:
                    player.water_buckets -= water
                    player.gold_quarters += water * PRICE_WATER
                    sold_items.append(f"{water} воды")
                    self.sound.play('sell')
                else:
                    self.show_message("Ошибка", f"Недостаточно воды! У вас: {player.water_buckets}", "error")
                    return
            
            if not sold_items:
                self.show_message("Ошибка", "Выберите товары для продажи (введите количество или отметьте лошадей)!", "warning")
                return
            
            items_text = ", ".join(sold_items)
            self.log_message(f"💰 {player.name} продал: {items_text}")
            self.show_toast(f"Продано: {items_text}", "💰", 5000)
            
            if not self.auction_mode:
                player.action_taken = True
            self.update_display()
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg='#2a3a2a')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="ВЫПОЛНИТЬ ПОКУПКУ", command=execute_buy,
                 bg='#4a7a2e', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=8).pack(side='left', padx=15)
        
        tk.Button(btn_frame, text="ВЫПОЛНИТЬ ПРОДАЖУ", command=execute_sell,
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=8).pack(side='left', padx=15)
        
        tk.Button(btn_frame, text="ЗАКРЫТЬ", command=dialog.destroy,
                 bg='#6E3E2E', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=8).pack(side='left', padx=15)
        self.apply_hover_effect_to_all_buttons(dialog)
    
    def sell_stable(self, pos, player, dialog):
        if player.remove_stable(pos):
            player.gold_quarters += PRICE_STABLE
            self.log_message(f"🏠 {player.name} продал стойло на позиции {pos+1}")
            self.sound.play('sell')
            self.show_toast("Стойло продано!", "🏠", 4000)
            dialog.destroy()
            self.update_display()
    
    def sell_field(self, pos, player, dialog):
        if player.remove_field(pos):
            player.gold_quarters += PRICE_FIELD
            self.log_message(f"🌾 {player.name} продал поле на позиции {pos+1}")
            self.sound.play('sell')
            self.show_toast("Поле продано!", "🌾", 4000)
            dialog.destroy()
            self.update_display()
    
    def buy_pending_upgrade(self, horse, player, dialog):
        if horse.pending_upgrades > 0 and player.gold_quarters >= PRICE_UPGRADE:
            self.choose_upgrade_type(horse, player)
            # Звук уже будет в choose_upgrade_type при выборе типа
            dialog.destroy()
            self.update_display()
        else:
            if horse.pending_upgrades <= 0:
                self.show_message("Ошибка", "Нет доступных прокачек!", "error")
            elif player.gold_quarters < PRICE_UPGRADE:
                self.sound.play('nomoney')
                self.show_message("Ошибка", "Недостаточно денег для прокачки!", "error")
    
    def choose_upgrade_type(self, horse, player):
        dialog = tk.Toplevel(self.root)
        dialog.title("🎯 ВЫБОР ПРОКАЧКИ")
        dialog.geometry("650x550")
        dialog.configure(bg='#2a3a2a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{horse.icon} {horse.name} - ВЫБЕРИТЕ УЛУЧШЕНИЕ", 
                font=('Arial', 16, 'bold'), bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        # Отображаем текущие прокачки
        current_frame = tk.Frame(dialog, bg='#2a3a2a')
        current_frame.pack(pady=10)
        
        tk.Label(current_frame, text="Текущие прокачки: ", font=('Arial', 12), bg='#2a3a2a', fg='white').pack(side='left')
        
        upgrades_frame = self.create_upgrades_display(current_frame, horse, font_size=14, bg_color='#2a3a2a')
        upgrades_frame.pack(side='left')
        
        stats = f"\n⚡{sum(1 for u in horse.upgrades if u=='speed')} 🥕{sum(1 for u in horse.upgrades if u=='radish')} 💧{sum(1 for u in horse.upgrades if u=='water')}"
        tk.Label(dialog, text=stats, font=('Arial', 12), bg='#2a3a2a', fg='white').pack()
        
        # ✅ ИСПРАВЛЕНО: ПРОВЕРЯЕМ ТОЛЬКО ПРИМЕНЁННЫЕ ПРОКАЧКИ (upgrades)
        # Белые прокачки (pending) - это уже купленные, но ещё не применённые
        # Они НЕ должны блокировать покупку новых, если есть свободные слоты
        if len(horse.upgrades) >= TRAINING_UPGRADES_MAX:
            self.show_message("Ошибка", f"{horse.name} уже достиг максимума прокачек ({TRAINING_UPGRADES_MAX}/{TRAINING_UPGRADES_MAX})!", "warning")
            dialog.destroy()
            return
        
        # Проверяем, какие улучшения доступны
        can_buy_speed = True  # Скорость всегда можно улучшать (нет ограничений)
        can_buy_radish = horse.food_per_day > 0  # Нельзя улучшать если еда уже 0
        can_buy_water = horse.water_per_day > 0  # Нельзя улучшать если вода уже 0
        
        upgrades = []
        if can_buy_speed:
            upgrades.append(("🔴 УВЕЛИЧИТЬ СКОРОСТЬ", 'speed', '#FF4444', f"+1 к скорости бега (сейчас {horse.total_speed})"))
        else:
            upgrades.append(("🔴 УВЕЛИЧИТЬ СКОРОСТЬ", 'speed', '#FF4444', f"+1 к скорости бега (сейчас {horse.total_speed})", False))
        
        if can_buy_radish:
            upgrades.append(("🟢 ЭКОНОМИЯ ЕДЫ", 'radish', '#00d632', f"-1 редиска/день (сейчас {horse.food_per_day})"))
        else:
            upgrades.append(("🟢 ЭКОНОМИЯ ЕДЫ", 'radish', '#888888', f"Уже не ест редиски (мин. 0)", False))
        
        if can_buy_water:
            upgrades.append(("🔵 ЭКОНОМИЯ ВОДЫ", 'water', '#4444FF', f"-1 ведро/день (сейчас {horse.water_per_day})"))
        else:
            upgrades.append(("🔵 ЭКОНОМИЯ ВОДЫ", 'water', '#888888', f"Уже не пьёт воду (мин. 0)", False))
        
        def apply_upgrade(up_type):
            # ✅ ИСПРАВЛЕНО: проверяем только ПРИМЕНЁННЫЕ прокачки (upgrades)
            if len(horse.upgrades) >= TRAINING_UPGRADES_MAX:
                self.show_message("Ошибка", f"{horse.name} уже достиг максимума прокачек ({TRAINING_UPGRADES_MAX}/{TRAINING_UPGRADES_MAX})!", "warning")
                dialog.destroy()
                return
            
            # ✅ Проверяем, что у лошади есть белые прокачки для применения
            if horse.pending_upgrades <= 0:
                self.show_message("Ошибка", f"У {horse.name} нет доступных белых прокачек для применения!", "warning")
                dialog.destroy()
                return
            
            if player.gold_quarters < PRICE_UPGRADE:
                self.sound.play('nomoney')
                self.show_message("Ошибка", "Не хватает денег для покупки прокачки!", "error")
                return

            player.gold_quarters -= PRICE_UPGRADE
            horse.upgrades.append(up_type)
            horse.upgrade_count = len(horse.upgrades)
            horse.pending_upgrades -= 1
            self.sound.play('upgrade')
            dialog.destroy()
            self.update_display()
            upgrade_names = {'speed': 'скорость', 'radish': 'экономию еды', 'water': 'экономию воды'}
            upgrade_name = upgrade_names.get(up_type, up_type)
            self.show_toast(f"{horse.name} получил улучшение: +{upgrade_name}!", "⚡", 4000)
        
        def cancel_upgrade():
            # ✅ Возвращаем белую прокачку обратно лошади (но только если она есть)
            if horse.pending_upgrades > 0:
                # Ничего не делаем - просто закрываем диалог
                dialog.destroy()
                self.update_display()
                self.show_toast(f"Улучшение для {horse.name} отменено", "❌", 3000)
            else:
                dialog.destroy()
        
        for upgrade in upgrades:
            if len(upgrade) == 5:  # Недоступное улучшение
                name, up_type, color, desc, available = upgrade
                frame = tk.Frame(dialog, bg='#3a4a3a', relief='ridge', bd=2)
                frame.pack(fill='x', pady=8, padx=20)
                
                tk.Label(frame, text=name, font=('Arial', 12, 'bold'), bg='#3a4a3a', fg=color).pack(side='left', padx=15, pady=12)
                tk.Label(frame, text=desc, font=('Arial', 10), bg='#3a4a3a', fg='#888888').pack(side='left', padx=10, pady=12)
                tk.Button(frame, text="НЕДОСТУПНО", 
                         state='disabled',
                         bg='#555555', fg='gray', font=('Arial', 11, 'bold'), padx=20).pack(side='right', padx=15)
            else:
                name, up_type, color, desc = upgrade
                frame = tk.Frame(dialog, bg='#3a4a3a', relief='ridge', bd=2)
                frame.pack(fill='x', pady=8, padx=20)
                
                tk.Label(frame, text=name, font=('Arial', 12, 'bold'), bg='#3a4a3a', fg=color).pack(side='left', padx=15, pady=12)
                tk.Label(frame, text=desc, font=('Arial', 10), bg='#3a4a3a', fg='white').pack(side='left', padx=10, pady=12)
                
                # ✅ Кнопка активна только если есть белые прокачки И не достигнут максимум
                if horse.pending_upgrades > 0 and len(horse.upgrades) < TRAINING_UPGRADES_MAX:
                    btn = tk.Button(frame, text="ВЫБРАТЬ", 
                                   command=lambda t=up_type: apply_upgrade(t),
                                   bg='#4a7a2e', fg='white', font=('Arial', 11, 'bold'), padx=20)
                else:
                    btn = tk.Button(frame, text="НЕТ БЕЛЫХ ПРОКАЧЕК", 
                                   state='disabled',
                                   bg='#555555', fg='gray', font=('Arial', 11, 'bold'), padx=20)
                btn.pack(side='right', padx=15)
        
        # Кнопка отмены
        btn_frame = tk.Frame(dialog, bg='#2a3a2a')
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="ЗАКРЫТЬ", 
                 command=cancel_upgrade,
                 bg='#8B4513', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=8).pack()
        self.apply_hover_effect_to_all_buttons(dialog)
    
    def show_available_tasks(self, player, parent_dialog):
        # ПРОВЕРКА: есть ли уже активное задание
        if player.temp_horse is not None:
            self.show_message("Ошибка", "У вас уже есть активное задание по опеке! Дождитесь его завершения.", "warning")
            return
        
        # ЕСЛИ НЕТ ЗАДАНИЙ - ГЕНЕРИРУЕМ ИХ
        if not self.available_tasks:
            self.generate_auction_tasks()
        
        # Фильтруем только доступные (не взятые) задания
        available_tasks = [task for task in self.available_tasks if not task['taken']]
        
        if not available_tasks:
            self.show_message("Ошибка", "Нет доступных заданий на этом аукционе!", "warning")
            return
        
        free_stable = player.get_free_stable()
        if free_stable == -1:
            self.show_message("Ошибка", "Нет свободных стойл для размещения лошади!", "warning")
            return
        
        task_dialog = tk.Toplevel(self.root)
        task_dialog.title("АУКЦИОН - ВЫБОР ЗАДАНИЯ")
        task_dialog.geometry("1000x800")
        task_dialog.configure(bg='#2a3a2a')
        task_dialog.transient(self.root)
        task_dialog.grab_set()
        
        tk.Label(task_dialog, text="🏪 ДОСТУПНЫЕ ЗАДАНИЯ 🏪", font=('Arial', 18, 'bold'),
                bg='#2a3a2a', fg='#FFD700').pack(pady=15)
        
        gold = player.gold_quarters // QUARTERS_PER_GOLD
        quarter = player.gold_quarters % QUARTERS_PER_GOLD
        tk.Label(task_dialog, text=f"💰 Ваши деньги: {gold}.{quarter} зол.",
                font=('Arial', 12), bg='#2a3a2a', fg='white').pack(pady=5)
        
        tk.Label(task_dialog, text=f"Свободных стойл: 1", font=('Arial', 12),
                bg='#2a3a2a', fg='#90EE90').pack(pady=5)
        
        # Проверяем, сегодня ли понедельник
        is_monday = (self.current_day % 7 == 1) or self.current_day == 1
        if not is_monday:
            tk.Label(task_dialog, text="⚠️ ВНИМАНИЕ: Аванс будет выплачен только в понедельник!", 
                    font=('Arial', 11, 'bold'), bg='#2a3a2a', fg='#FF4444').pack(pady=5)
        
        task_names = {"care": "🏠 Содержание", "train": "🏇 Тренировка", "win_race": "🏆 Победа в скачках"}
        
        def select_task(task_index, task_data):
            horse = task_data['horse']
            
            # ✅ Проверяем наличие ключей с обратной совместимостью
            if 'original_horse' in task_data and 'owner' in task_data:
                original_horse = task_data['original_horse']
                owner = task_data['owner']
            else:
                original_horse = None
                owner = None
                for o in self.horse_owners.values():
                    if o.name == task_data['owner_name']:
                        owner = o
                        for h in o.horses:
                            if h.name == horse.name:
                                original_horse = h
                                break
                        break
                
                if original_horse is None:
                    original_horse = Horse(horse.level, horse.name, horse.owner_color, False)
                    original_horse.upgrades = horse.upgrades.copy()
                    original_horse.training_progress = horse.training_progress
                    original_horse.pending_upgrades = horse.pending_upgrades
                    if owner:
                        owner.horses.append(original_horse)
            
            task_type = task_data['task_type']
            advance = task_data['advance']
            reward = task_data['reward']
            weekly_cost = task_data['weekly_cost']
            owner_name = task_data['owner_name']
            
            # Помечаем задание как взятое
            task_data['taken'] = True
            
            # Лошадь появляется сразу в стойле
            player.horse_positions[free_stable] = len(player.horses)
            player.horses.append(horse)
            
            # СОЗДАЁМ ОБЪЕКТ ЗАДАНИЯ С СОХРАНЕНИЕМ ССЫЛОК
            player.temp_horse = TempHorse(horse, task_type, advance, reward, owner_name, weekly_cost)
            player.temp_horse.start_pending_upgrades = horse.pending_upgrades

            # ✅ СОХРАНЯЕМ ОБЩЕЕ КОЛИЧЕСТВО ПРОКАЧЕК ДЛЯ ОРИГИНАЛЬНОЙ ЛОШАДИ
            if original_horse:
                player.temp_horse.start_total_upgrades = len(original_horse.upgrades) + original_horse.pending_upgrades
            else:
                player.temp_horse.start_total_upgrades = horse.pending_upgrades
            
            player.temp_horse.original_horse = original_horse
            player.temp_horse.owner = owner
            
            # Аванс выплачивается ТОЛЬКО в понедельник
            if is_monday:
                player.gold_quarters += advance
                player.temp_horse.advance_paid = True
                advance_gold = advance // QUARTERS_PER_GOLD
                advance_q = advance % QUARTERS_PER_GOLD
                if advance_q > 0:
                    advance_text = f"Аванс получен: {advance_gold}.{advance_q} зол."
                else:
                    advance_text = f"Аванс получен: {advance_gold} зол."
                self.log_message(f"💰 {player.name} получил аванс {advance_gold}.{advance_q} зол. за опеку {horse.name}")
                self.show_toast(f"Аванс получен! +{advance_gold}.{advance_q} зол.", "💰", 5000)
            else:
                player.temp_horse.advance_paid = False
                advance_gold = advance // QUARTERS_PER_GOLD
                advance_q = advance % QUARTERS_PER_GOLD
                if advance_q > 0:
                    advance_text = f"Аванс будет выплачен в понедельник: {advance_gold}.{advance_q} зол."
                else:
                    advance_text = f"Аванс будет выплачен в понедельник: {advance_gold} зол."
            
            # ✅ ФОРМИРУЕМ ПРАВИЛЬНОЕ СООБЩЕНИЕ О НАГРАДЕ
            if task_type == "train":
                # Для тренировки награда зависит от уровня лошади
                level = horse.level
                if level == 1:
                    reward_text = "2 зол. за прокачку"
                elif level == 2:
                    reward_text = "1 зол. за прокачку"
                else:  # level == 3
                    reward_text = "2 четвертака за прокачку"
            else:
                # Для других заданий показываем общую награду
                reward_gold = reward // QUARTERS_PER_GOLD
                reward_q = reward % QUARTERS_PER_GOLD
                if reward_q > 0:
                    reward_text = f"{reward_gold}.{reward_q} зол."
                else:
                    reward_text = f"{reward_gold} зол."

            self.log_message(f"📋 {player.name} взял лошадь {horse.name} (Ур.{horse.level}) на попечение у {owner_name}!\nЗадание: {task_names[task_type]}, {advance_text}, Награда: {reward_text}")
            
            self.show_message("ЗАДАНИЕ ПРИНЯТО!", 
                            f"Вы взяли {horse.name} (Ур.{horse.level})!\n"
                            f"Задание: {task_names[task_type]}\n"
                            f"{advance_text}\n"
                            f"Награда за выполнение: {reward_text}\n\n"
                            f"Лошадь размещена в свободном стойле.\n"
                            f"Если не выполните задание - потеряете аванс (если он был выплачен)!", 
                            "info")
            task_dialog.destroy()
            parent_dialog.destroy()
            self.update_display()
            
        # Canvas для прокрутки
        canvas = tk.Canvas(task_dialog, bg='#2a3a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(task_dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a3a2a')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        for i, task_data in enumerate(available_tasks):
            horse = task_data['horse']
            task_type = task_data['task_type']
            advance = task_data['advance']
            reward = task_data['reward']
            weekly_cost = task_data['weekly_cost']
            level = horse.level
            owner_name = task_data['owner_name']
            
            frame = tk.Frame(scrollable_frame, bg='#3a4a3a', relief='ridge', bd=2)
            frame.pack(fill='x', pady=8, padx=10)
            
            task_text = f"{task_names[task_type]}"
            
            advance_gold = advance // QUARTERS_PER_GOLD
            advance_q = advance % QUARTERS_PER_GOLD
            if advance_q > 0:
                advance_text_display = f"{advance_gold}.{advance_q} зол."
            else:
                advance_text_display = f"{advance_gold} зол."
            
            if not is_monday:
                advance_text_display += " (в понедельник)"
            
            info_frame = tk.Frame(frame, bg='#3a4a3a')
            info_frame.pack(side='left', padx=10, pady=8)
            
            info_lines = f"{horse.icon} {horse.name} (Ур.{horse.level})\n"
            info_lines += f"👑 Владелец: {owner_name}\n"
            info_lines += f"📋 {task_text}\n"
            info_lines += f"💰 Аванс: {advance_text_display} | "

            if task_type == "train":
                if level == 1:
                    reward_per_upgrade = 2 * QUARTERS_PER_GOLD
                    reward_text = f"2 зол. за прокачку (макс 8 зол.)"
                elif level == 2:
                    reward_per_upgrade = 1 * QUARTERS_PER_GOLD
                    reward_text = f"1 зол. за прокачку (макс 4 зол.)"
                else:
                    reward_per_upgrade = 2
                    reward_text = f"2 четвертака за прокачку (макс 2 зол.)"
                info_lines += f"🏆 Награда: {reward_text}\n"
            else:
                reward_gold = reward // QUARTERS_PER_GOLD
                reward_q = reward % QUARTERS_PER_GOLD
                if reward_q > 0:
                    reward_text = f"{reward_gold}.{reward_q} зол."
                else:
                    reward_text = f"{reward_gold} зол."
                info_lines += f"🏆 Награда: {reward_text}\n"
            
            weekly_gold = weekly_cost // QUARTERS_PER_GOLD
            weekly_q = weekly_cost % QUARTERS_PER_GOLD
            if weekly_q > 0:
                weekly_text = f"{weekly_gold}.{weekly_q} зол."
            else:
                weekly_text = f"{weekly_gold} зол."
            info_lines += f"💧 Расход на неделю: ~{weekly_text}"
            
            tk.Label(info_frame, text=info_lines, font=('Arial', 10), bg='#3a4a3a', fg='white', justify='left').pack(anchor='w')
            
            upgrades_frame = tk.Frame(info_frame, bg='#3a4a3a')
            upgrades_frame.pack(anchor='w', pady=(5, 0))
            
            tk.Label(upgrades_frame, text="⭐ Прокачки: ", font=('Arial', 10), bg='#3a4a3a', fg='white').pack(side='left')
            
            upgrades_display = self.create_upgrades_display(upgrades_frame, horse, font_size=10, bg_color='#3a4a3a')
            upgrades_display.pack(side='left')
            
            btn = tk.Button(frame, text="ВЗЯТЬ ЗАДАНИЕ", 
                           command=lambda idx=i, td=task_data: select_task(idx, td),
                           bg='#4a7a2e', fg='white', font=('Arial', 11, 'bold'), padx=15)
            btn.pack(side='right', padx=15)
        
        tk.Button(task_dialog, text="ПРОПУСТИТЬ", 
                 command=task_dialog.destroy,
                 bg='#8B4513', fg='white', font=('Arial', 11, 'bold'), padx=25, pady=8).pack(pady=20)
        self.apply_hover_effect_to_all_buttons(task_dialog)
    
    def end_turn(self):
        if not self.game_active:
            return
        player = self.players[self.current_player_idx]
        
        # Используем метод с выбором
        all_fed, feed_msg, dead_horses = player.feed_horses_with_choice(self)
        self.log_message(feed_msg)
        
        if not all_fed:
            self.show_message("ЛОШАДИ ПОГИБЛИ!", feed_msg, "error")
            self.show_toast("Некоторые лошади погибли от голода!", "💀", 5000)
            self.sound.play('nash_geroi_mertv')
            self.check_bankruptcy()
        
        player.action_taken = False
        self.current_player_idx += 1
        
        if self.current_player_idx >= len(self.players):
            self.current_player_idx = 0
            self.next_day()
        
        # ✅ Сбрасываем флаг предупреждения для этого хода
        self._warning_shown_this_turn = False
        self.warning_shown_today = False
        self.update_display()
        
    def auto_upgrade_horse(self, horse, owner):
        """
        Автоматически улучшает лошадь владельца
        Возвращает список применённых улучшений и их количество
        """
        applied_upgrades = []
        upgrade_names = {
            'speed': 'скорость',
            'radish': 'экономию еды', 
            'water': 'экономию воды'
        }
        
        upgrade_count = 0
        
        while horse.pending_upgrades > 0:
            if len(horse.upgrades) >= TRAINING_UPGRADES_MAX:
                break
            
            available_upgrades = []
            
            # Скорость - всегда доступна
            available_upgrades.append('speed')
            
            # Еда - доступна, если лошадь ЕСТ редиски (food_per_day > 0)
            if horse.food_per_day > 0:
                available_upgrades.append('radish')
            
            # Вода - доступна, если лошадь ПЬЁТ воду (water_per_day > 0)
            if horse.water_per_day > 0:
                available_upgrades.append('water')
            
            # Если нет доступных улучшений (только скорость)
            if not available_upgrades:
                available_upgrades.append('speed')
            
            # Случайный выбор
            upgrade_type = random.choice(available_upgrades)
            
            # Применяем
            horse.upgrades.append(upgrade_type)
            horse.upgrade_count = len(horse.upgrades)
            horse.pending_upgrades -= 1
            upgrade_count += 1
            
            applied_upgrades.append(upgrade_names.get(upgrade_type, upgrade_type))
        
        return applied_upgrades, upgrade_count  # ✅ Возвращаем информацию

    def weekly_results(self):
        self.log_message("=" * 50)
        self.log_message("🏆 ВОСКРЕСЕНЬЕ! НАЧАЛО СКАЧЕК 🏆")
        
        # Сохраняем начальное количество прокачек для временных лошадей
        for player in self.players:
            if player.temp_horse:
                if not hasattr(player.temp_horse, 'start_pending_upgrades'):
                    player.temp_horse.start_pending_upgrades = player.temp_horse.horse.pending_upgrades
                else:
                    player.temp_horse.start_pending_upgrades = player.temp_horse.horse.pending_upgrades
        
        # Применяем накопленные тренировки (для всех лошадей)
        for player in self.players:
            for horse in player.horses:
                if horse.weekly_training_gain > 0:
                    horse.training_progress += horse.weekly_training_gain
                    while horse.training_progress >= TRAINING_CIRCLE_MAX:
                        if len(horse.upgrades) + horse.pending_upgrades >= TRAINING_UPGRADES_MAX:
                            horse.training_progress = TRAINING_CIRCLE_MAX - 1
                            break
                        horse.training_progress -= TRAINING_CIRCLE_MAX
                        horse.pending_upgrades += 1
                        self.log_message(f"🎉 {horse.name}: получена белая прокачка! Всего доступно: {horse.pending_upgrades}")
                        self.show_toast(f"{horse.name} получил белую прокачку!", "🎉", 5000)
                    horse.weekly_training_gain = 0
        
        # Запускаем режим скачек (голосование)
        self.race_mode = True
        self.race_participants = []
        self.current_player_idx = 0
        for player in self.players:
            player.action_taken = False
        self.update_actions_buttons()
        self.update_display()
        
        self.show_overlay_message("СКАЧКИ", "Игроки, выбирайте участвовать или пропустить!")

    def next_day(self):
        self.current_day += 1
        
        self.tasks_generated = False
        self.available_tasks = []

        for player in self.players:
            player.action_taken = False
        
        # ✅ Сбрасываем флаги предупреждений на новый день
        self.warning_shown_today = False
        self._warning_shown_this_turn = False
        
        # ✅ Если наступил понедельник - выключаем аукцион
        if (self.current_day - 1) % 7 == 0:
            self.auction_mode = False
            self.race_mode = False
            self.update_actions_buttons()

        # ✅ ВЫПЛАТА АВАНСА В ПОНЕДЕЛЬНИК
        # Понедельник - когда (self.current_day - 1) % 7 == 0
        if (self.current_day - 1) % 7 == 0:
            for player in self.players:
                if player.temp_horse and player.temp_horse.advance > 0:
                    if not player.temp_horse.advance_paid:
                        player.gold_quarters += player.temp_horse.advance
                        player.temp_horse.advance_paid = True
                        advance_gold = player.temp_horse.advance // QUARTERS_PER_GOLD
                        advance_q = player.temp_horse.advance % QUARTERS_PER_GOLD
                        self.log_message(f"💰 {player.name} получил аванс {advance_gold}.{advance_q} зол. за опеку {player.temp_horse.horse.name}")
                        self.show_toast(f"Получен аванс за опеку! +{advance_gold}.{advance_q} зол.", "💰", 5000)
        
        # ✅ Воскресенье - когда (self.current_day - 1) % 7 == 6
        # И ТОЛЬКО если не в режиме аукциона (чтобы не запускать повторно)
        if (self.current_day - 1) % 7 == 6 and not self.auction_mode:
            self.weekly_results()
            return  # ✅ Выходим, чтобы не выполнять остальной код
        
        # Понедельник для посадки редисок
        if (self.current_day - 1) % 7 == 0 and self.current_day > 1:
            self.week_number = self.current_day // 7 + 1
            self.log_message(f"🌱 НАЧАЛО НЕДЕЛИ {self.week_number}! Вы можете посадить редиски.")
        
        if self.current_day > self.days_total:
            self.end_game()
        
        self.log_message(f"📅 Наступил день {self.current_day}")
        self.update_display()
    
    def harvest_phase(self):
        self.log_message("🌾 СБОР УРОЖАЯ 🌾")
        
        for player in self.players:
            total_harvest = 0
            total_earned = 0
            price_details = []  # Для хранения информации о цене на каждом поле
            
            for field_pos, radishes in list(player.radish_positions.items()):
                if radishes:
                    count = len(radishes)
                    dice = random.randint(1, 6)
                    price_map = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: QUARTERS_PER_GOLD}
                    price = price_map[dice]
                    earned = count * price
                    player.gold_quarters += earned
                    total_harvest += count
                    total_earned += earned
                    
                    # Запоминаем цену на этом поле
                    price_text = ""
                    if price == 0:
                        price_text = "0 четвертаков (неудачно)"
                    elif price == 1:
                        price_text = "1 четвертак"
                    elif price == 2:
                        price_text = "2 четвертака"
                    elif price == QUARTERS_PER_GOLD:
                        price_text = "4 четвертака (максимум!)"
                    price_details.append(f"поле {field_pos + 1}: {count} шт. по {price_text}")
                    
                    self.log_message(f"🥕 {player.name}: собрал {count} редисок с поля {field_pos + 1}, цена {price} четвертаков/шт, выручка {earned//QUARTERS_PER_GOLD}.{earned%QUARTERS_PER_GOLD} зол.")
            
            if total_harvest > 0:
                # Формируем детальное сообщение
                details_text = " | ".join(price_details)
                self.log_message(f"🌾 {player.name}: ИТОГО собрано {total_harvest} редисок, выручка {total_earned//QUARTERS_PER_GOLD}.{total_earned%QUARTERS_PER_GOLD} зол. ({details_text})")
                
                # Показываем тост с деталями
                toast_msg = f"🌾 Собрано {total_harvest} редисок!\nВыручка: {total_earned//QUARTERS_PER_GOLD}.{total_earned%QUARTERS_PER_GOLD} зол.\n\n"
                for detail in price_details:
                    toast_msg += f"• {detail}\n"
                self.show_toast(toast_msg, "🌾", 6000)
            
            player.radish_positions.clear()
    
    def bot_turn(self):
        if not self.game_active:
            return
        player = self.players[self.current_player_idx]
        if player.is_bot and not player.action_taken and not player.is_bankrupt:
            if self.race_mode:
                if random.random() < 0.5 and player.horses and player.gold_quarters >= PRICE_RACE_ENTRY:
                    own_horses = [h for h in player.horses if not h.is_temp]
                    if own_horses:
                        # Проверка на повторное участие той же лошади
                        last_horse_name = self.last_race_horse.get(player.name, None)
                        available_horses = [h for h in own_horses if h.name != last_horse_name]
                        if available_horses:
                            horse = random.choice(available_horses)
                            player.gold_quarters -= PRICE_RACE_ENTRY
                            self.race_participants.append((player, horse))
                            self.last_race_horse[player.name] = horse.name
                            self.log_message(f"🤖 {player.name} участвует в скачках с {horse.name}")
                        else:
                            self.log_message(f"🤖 {player.name} пропускает скачки (нет доступных лошадей)")
                    else:
                        self.log_message(f"🤖 {player.name} пропускает скачки (нет лошадей)")
                else:
                    self.log_message(f"🤖 {player.name} пропускает скачки")
                
                player.action_taken = True
                self.update_display()
                self.end_race_phase()  # Вызываем переход к следующему игроку
                return
            elif self.auction_mode:
                if random.random() < 0.3:
                    self.bot_market()
                else:
                    player.action_taken = True
                    self.update_display()
                    self.end_auction_turn()
                return
            else:
                total_radish_need = sum(h.food_per_day for h in player.horses)
                total_water_need = sum(h.water_per_day for h in player.horses)
                
                need_radish = player.radishes < total_radish_need
                need_water = player.water_buckets < total_water_need
                
                if need_radish or need_water:
                    bought = False
                    if need_radish and player.gold_quarters >= 5:
                        buy = min(15, total_radish_need - player.radishes + 5)
                        if player.gold_quarters >= buy:
                            player.gold_quarters -= buy
                            player.radishes += buy
                            self.log_message(f"🤖 {player.name} купил {buy} редисок")
                            bought = True
                            self.show_toast(f"{player.name} купил {buy} редисок", "🥕", 4000)
                    if need_water and player.gold_quarters >= 5:
                        buy = min(15, total_water_need - player.water_buckets + 5)
                        if player.gold_quarters >= buy:
                            player.gold_quarters -= buy
                            player.water_buckets += buy
                            self.log_message(f"🤖 {player.name} купил {buy} воды")
                            bought = True
                            self.show_toast(f"{player.name} купил {buy} воды", "💧", 4000)
                    if bought:
                        player.action_taken = True
                        self.update_display()
                        self.end_turn()
                        return
                    else:
                        self.bot_sell_assets()
                        return
                
                if player.horses:
                    horse = random.choice(player.horses)
                    dice = random.randint(1, 6)
                    total = dice + horse.total_speed
                    if total <= 0:
                        self.log_message(f"🤖 {player.name} пытался тренировать {horse.name}, но лошадь отказалась бежать!")
                    else:
                        horse.training_progress += total
                        self.log_message(f"🤖 {player.name} тренирует {horse.name}: бросок {dice} + скорость {horse.total_speed} = {total}")
                    player.action_taken = True
                    self.update_display()
                    self.end_turn()
                    return
                
                actions = []
                if player.gold_quarters >= PRICE_RADISH:
                    actions.append(self.bot_market)
                if player.gold_quarters >= PRICE_RADISH:
                    actions.append(self.bot_lottery)
                if player.fields > 0 and player.radishes > 0 and player.water_buckets > 0 and self.current_day % 7 == 1:
                    actions.append(self.bot_plant)
                
                if actions:
                    random.choice(actions)()
                else:
                    self.bot_end_turn()
    
    def bot_sell_assets(self):
        player = self.players[self.current_player_idx]
        
        if player.radishes > 0:
            sell_qty = min(player.radishes, 10)
            player.radishes -= sell_qty
            player.gold_quarters += sell_qty
            self.log_message(f"🤖 {player.name} продал {sell_qty} редисок")
            self.show_toast(f"{player.name} продал {sell_qty} редисок", "🥕", 4000)
            self.bot_turn()
            return
        
        if player.water_buckets > 0:
            sell_qty = min(player.water_buckets, 10)
            player.water_buckets -= sell_qty
            player.gold_quarters += sell_qty
            self.log_message(f"🤖 {player.name} продал {sell_qty} воды")
            self.show_toast(f"{player.name} продал {sell_qty} воды", "💧", 4000)
            self.bot_turn()
            return
        
        empty_stables = [i for i in range(MAX_LAND) if player.land_map[i] == 1 and i not in player.horse_positions]
        if empty_stables:
            pos = empty_stables[0]
            player.remove_stable(pos)
            player.gold_quarters += PRICE_STABLE
            self.log_message(f"🤖 {player.name} продал стойло")
            self.show_toast(f"{player.name} продал стойло", "🏠", 4000)
            self.bot_turn()
            return
        
        empty_fields = [i for i in range(MAX_LAND) if player.land_map[i] == 2 and i not in player.radish_positions]
        if empty_fields:
            pos = empty_fields[0]
            player.remove_field(pos)
            player.gold_quarters += PRICE_FIELD
            self.log_message(f"🤖 {player.name} продал поле")
            self.show_toast(f"{player.name} продал поле", "🌾", 4000)
            self.bot_turn()
            return
        
        self.bot_end_turn()
    
    def bot_market(self):
        player = self.players[self.current_player_idx]
        if player.radishes < 30 and player.gold_quarters >= 10:
            player.radishes += 10
            player.gold_quarters -= 10
            self.log_message(f"🤖 {player.name} купил 10 редисок")
            self.show_toast(f"{player.name} купил 10 редисок", "🥕", 4000)
        elif player.water_buckets < 30 and player.gold_quarters >= 10:
            player.water_buckets += 10
            player.gold_quarters -= 10
            self.log_message(f"🤖 {player.name} купил 10 воды")
            self.show_toast(f"{player.name} купил 10 воды", "💧", 4000)
        else:
            self.bot_end_turn()
            return
        
        if not self.auction_mode:
            player.action_taken = True
            self.update_display()
            self.end_turn()
        else:
            player.action_taken = False
            self.update_display()
    
    def bot_lottery(self):
        player = self.players[self.current_player_idx]
        max_tickets = min(2, player.gold_quarters // PRICE_RADISH)
        if max_tickets > 0:
            tickets = random.randint(1, max_tickets)
            cost = tickets * PRICE_RADISH
            player.gold_quarters -= cost
            
            prizes = {1: 0, 2: 1, 3: 0, 4: 2, 5: 0, 6: QUARTERS_PER_GOLD}
            total_win = 0
            win_radish = 0
            win_water = 0
            
            for _ in range(tickets):
                roll = random.randint(1, 6)
                if roll == 3:
                    player.radishes += 1
                    win_radish += 1
                elif roll == 5:
                    player.water_buckets += 1
                    win_water += 1
                else:
                    win = prizes[roll]
                    player.gold_quarters += win
                    total_win += win
            
            self.log_message(f"🤖 {player.name} купил {tickets} билет(ов) лотереи, выиграл {total_win} четвертаков, {win_radish} редисок, {win_water} воды")
            if total_win > 0 or win_radish > 0 or win_water > 0:
                self.sound.play('lucky')
                self.show_toast(f"{player.name} выиграл {total_win} четвертаков!", "🎰", 4000)
            else:
                self.sound.play('unlucky')
                self.show_toast(f"{player.name} ничего не выиграл", "😞", 4000)
        else:
            self.bot_end_turn()
            return
        
        player.action_taken = True
        self.update_display()
        self.end_turn()
    
    def bot_plant(self):
        player = self.players[self.current_player_idx]
        free_fields = player.get_free_fields()
        if free_fields:
            field = random.choice(free_fields)
            max_plant = min(RADISH_PER_FIELD, player.radishes, player.water_buckets)
            if max_plant > 0:
                plant = random.randint(1, max_plant)
                planted = player.plant_radishes(field, plant)
                if planted > 0:
                    self.log_message(f"🤖 {player.name} посадил {planted} редисок на поле {field + 1}")
                    self.show_toast(f"{player.name} посадил {planted} редисок", "🌱", 4000)
            player.action_taken = True
            self.update_display()
            self.end_turn()
        else:
            self.bot_end_turn()
    
    def bot_end_turn(self):
        player = self.players[self.current_player_idx]
        player.action_taken = True
        self.update_display()
        self.end_turn()
    
    def end_game(self):
        if not self.game_active:
            return
        
        # Закрываем все побочные окна
        self.close_all_windows()
        
        # Показываем финальный оверлей
        self.show_end_game_overlay()

class NameDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, default="", sound_manager=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.configure(bg='#2a3a2a')
        self.transient(parent)
        self.grab_set()

        self.sound = sound_manager
        self.result = None  # <-- Изначально None
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (300 // 2)
        self.geometry(f"+{x}+{y}")
        
        tk.Label(self, text=prompt, font=('Arial', 14), bg='#2a3a2a', fg='white').pack(pady=25)
        
        self.entry = tk.Entry(self, width=30, font=('Arial', 12), cursor="xterm")
        self.entry.pack(pady=10)
        self.entry.insert(0, default)
        self.entry.select_range(0, tk.END)
        
        btn_frame = tk.Frame(self, bg='#2a3a2a')
        btn_frame.pack(pady=25)
        
        # Стилизованные кнопки
        ok_btn = self.create_styled_button(btn_frame, "ПОДТВЕРДИТЬ", self.ok, '#4a7a2e')
        ok_btn.pack(side='left', padx=15)
        
        cancel_btn = self.create_styled_button(btn_frame, "ОТМЕНА", self.cancel, '#8B4513')
        cancel_btn.pack(side='left', padx=15)
    
    def create_styled_button(self, parent, text, command, color):
        """Создаёт стилизованную кнопку"""
        hover_color = '#5a9a3e' if color == '#4a7a2e' else '#a06030'
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg='white', font=('Arial', 12, 'bold'), 
                       padx=25, pady=5, cursor="hand2",
                       activebackground=hover_color, activeforeground='white')
        
        def on_enter(e):
            btn.config(bg=hover_color)
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def ok(self):
        if self.sound:
            self.sound.play('click')
        self.result = self.entry.get().strip()
        if not self.result:
            self.result = "Фермер"
        self.destroy()
    
    def cancel(self):
        if self.sound:
            self.sound.play('click')
        self.result = None  # <-- Важно: None при отмене
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = HorseBoardGame(root)
    root.mainloop()