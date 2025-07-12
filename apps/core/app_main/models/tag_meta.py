from django.db import models

class TagPageMeta(models.Model):
    tag = models.OneToOneField("Tag", on_delete=models.CASCADE, related_name="meta")
    related_tags = models.ManyToManyField("Tag", blank=True, related_name="tagged_tag_pages")

    class Meta:
        verbose_name = "Page de tag - métadonnées"
        verbose_name_plural = "Pages de tag - métadonnées"

    def __str__(self):
        return f"Meta pour la page de tag : {self.tag.name}"
    