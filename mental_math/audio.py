"""Optional pygame audio with graceful fallback when a device is unavailable."""

from pathlib import Path
import sys


def asset_path(relative_path: str) -> Path:
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
    return bundle_root / relative_path


class AudioManager:
    def __init__(self) -> None:
        self._pygame = None

    def set_music(self, enabled: bool) -> bool:
        if not enabled:
            if self._pygame is not None:
                try:
                    self._pygame.mixer.music.fadeout(450)
                except Exception:
                    pass
            return True
        try:
            if self._pygame is None:
                import pygame

                pygame.mixer.pre_init(frequency=11025, size=8, channels=1, buffer=512)
                pygame.mixer.init()
                self._pygame = pygame
            music = self._pygame.mixer.music
            if not music.get_busy():
                music.load(str(asset_path("assets/ambient.wav")))
                music.set_volume(0.16)
                music.play(loops=-1, fade_ms=900)
            return True
        except Exception:
            return False

    def play_tone(self) -> bool:
        try:
            import winsound

            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            return True
        except Exception:
            return False

    def close(self) -> None:
        if self._pygame is not None:
            try:
                self._pygame.mixer.music.fadeout(250)
                self._pygame.mixer.quit()
            except Exception:
                pass
