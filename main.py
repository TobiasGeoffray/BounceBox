"""Point d'entrée pour l'application Qt du BounceBox."""
import sys
import os
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
# test
if __name__ == "__main__":
    # Vérifier si nous sommes dans un environnement graphique
    if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
        print("❌ Aucun environnement graphique détecté (DISPLAY ou WAYLAND_DISPLAY)")
        print("💡 Essayez de lancer avec:")
        print("   export DISPLAY=:0")
        print("   export DISPLAY=:0")

        print("   ou utilisez un serveur X11/Wayland")
        sys.exit(1)

    try:
        app = QApplication(sys.argv)
        print("✅ QApplication créée")

        window = MainWindow()
        print("✅ MainWindow créée")

        window.show()
        print("✅ Fenêtre affichée")

        print("🎮 Jeu BounceBox prêt ! Fermez la fenêtre pour quitter.")
        sys.exit(app.exec_())

    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
