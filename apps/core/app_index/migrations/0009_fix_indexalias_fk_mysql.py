# apps/content/app_index/migrations/XXXX_fix_indexalias_fk_mysql.py
from django.db import migrations

class Migration(migrations.Migration):
    # ⚠️ Mets ici la migration qui a créé IndexAlias (celle qui a échoué) comme dépendance.
    # Exemple : dependencies = [("app_index", "0007_create_indexalias")]
    dependencies = [
        ("app_index", "0008_indexalias"),
    ]

    operations = [
        migrations.RunSQL(
            # 1) Aligner le type sur le parent (INT)
            sql="""
                ALTER TABLE `app_index_indexalias`
                MODIFY COLUMN `entry_id` INT NOT NULL;
            """,
            reverse_sql="""
                ALTER TABLE `app_index_indexalias`
                MODIFY COLUMN `entry_id` BIGINT NOT NULL;
            """,
        ),
        migrations.RunSQL(
            # 2) Ajouter la contrainte FK (nommée comme celle que Django a tenté d'ajouter)
            sql="""
                ALTER TABLE `app_index_indexalias`
                ADD CONSTRAINT `app_index_indexalias_entry_id_1a8ea904_fk_app_index`
                FOREIGN KEY (`entry_id`) REFERENCES `app_index_indexentry` (`id`)
                ON DELETE CASCADE;
            """,
            reverse_sql="""
                ALTER TABLE `app_index_indexalias`
                DROP FOREIGN KEY `app_index_indexalias_entry_id_1a8ea904_fk_app_index`;
            """,
        ),
    ]
