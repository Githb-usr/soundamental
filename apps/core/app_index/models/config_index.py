from django.db import models
from .base_models import Category

# ====================================================
# Configuration d'affichage des sous-lettres de l'index
# ====================================================

class IndexSettings(models.Model):
    """
    Configuration pour afficher ou masquer les sous-lettres dans l'index général et les catégories.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        help_text="Nom de la catégorie (ex: 'artistes', 'labels', etc.). Laisser vide pour l'index général."
    )
    apply_to_all = models.BooleanField(
        default=False,
        help_text="Cochez cette case pour activer les sous-lettres partout (toutes les lettres, chiffres et @)."
    )
    letters_with_sub_buttons = models.TextField(
        blank=True,
        help_text="Liste des lettres/chiffres activant les sous-lettres (ex: 'A,B,C,1,2,3')."
    )

    def get_active_letters(self):
        """Renvoie la liste des lettres/chiffres avec sous-lettres activés."""
        return self.letters_with_sub_buttons.split(",") if self.letters_with_sub_buttons else []

    def save(self, *args, **kwargs):
        if self.apply_to_all:
            self.letters_with_sub_buttons = "0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,@"
        super().save(*args, **kwargs)
        # Recharge l’objet depuis la base pour mettre à jour l'admin
        self.refresh_from_db()

    class Meta:
        unique_together = ("category",)
        indexes = [
            models.Index(fields=["category"]),
        ]
        verbose_name = "Configuration de l'index"
        verbose_name_plural = "Index - Configuration"

    def __str__(self):
        return f"Config Index: {self.category.name if self.category else 'Index Général'}"
