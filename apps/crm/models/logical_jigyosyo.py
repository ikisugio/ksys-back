from django.db import models
from .jigyosyo import Jigyosyo
from ..consts import TYPE_PRIORITY


class LogicalJigyosyo(models.Model):
    jigyosyos = models.ManyToManyField("crm.Jigyosyo", related_name="logical_groups")
    representative = models.ForeignKey("crm.Jigyosyo", on_delete=models.SET_NULL, null=True, related_name="main_representative_for")

    def set_representative(self):
        sorted_jigyosyos = sorted(self.jigyosyos.all(), key=lambda j: self.TYPE_PRIORITY.index(j.type) if j.type in self.TYPE_PRIORITY else float('inf'))
        self.representative = sorted_jigyosyos[0]

    @classmethod
    def create_grouped_jigyosyo(cls):
        jigyosyos = Jigyosyo.objects.all().prefetch_related('company')
        grouped_data = {}
        
        for jigyosyo in jigyosyos:
            key = (jigyosyo.address, jigyosyo.company.company_code if jigyosyo.company.company_code else jigyosyo.company.address)
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(jigyosyo)
        
        for group in grouped_data.values():
            logical_jigyosyo = cls.objects.create()
            logical_jigyosyo.jigyosyos.set(group)
            logical_jigyosyo.set_representative()
            logical_jigyosyo.save()

    def merge(self, jigyosyos_to_merge):
        # Merge the selected Jigyosyo instances into this LogicalJigyosyo
        self.jigyosyos.add(*jigyosyos_to_merge)
        self.set_representative()
        self.save()
        
        # Create a new action instance for this merge
        action = LogicalJigyosyoAction.objects.create(
            action='merge',
            logical_jigyosyo=self
        )
        action.affected_jigyosyos.set(jigyosyos_to_merge)
        action.save()

    def split(self, jigyosyo_to_split):
        # Remove the selected Jigyosyo instance from this LogicalJigyosyo
        self.jigyosyos.remove(jigyosyo_to_split)
        new_logical_jigyosyo = LogicalJigyosyo.objects.create()
        new_logical_jigyosyo.jigyosyos.add(jigyosyo_to_split)
        new_logical_jigyosyo.set_representative()
        new_logical_jigyosyo.save()

        # Create a new action instance for this split
        action = LogicalJigyosyoAction.objects.create(
            action='split',
            logical_jigyosyo=self
        )
        action.affected_jigyosyos.set([jigyosyo_to_split])
        action.save()

    def undo_last_action(self):
        last_action = self.actions.last()
        
        if last_action.action == 'merge':
            affected_jigyosyos = last_action.affected_jigyosyos.all()
            self.jigyosyos.remove(*affected_jigyosyos)
            self.set_representative()
            self.save()
            last_action.delete()

        elif last_action.action == 'split':
            affected_jigyosyo = last_action.affected_jigyosyos.first()
            self.jigyosyos.add(affected_jigyosyo)
            affected_jigyosyo.logical_groups.first().delete()
            self.set_representative()
            self.save()
            last_action.delete()

class LogicalJigyosyoAction(models.Model):
    ACTION_CHOICES = [
        ('merge', 'Merge'),
        ('split', 'Split'),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    logical_jigyosyo = models.ForeignKey("crm.LogicalJigyosyo", on_delete=models.CASCADE, related_name="actions")
    affected_jigyosyos = models.ManyToManyField("crm.Jigyosyo", related_name="related_actions")
    created_at = models.DateTimeField(auto_now_add=True)
