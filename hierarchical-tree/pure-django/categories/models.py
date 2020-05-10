from django.db import models
from django.forms.models import model_to_dict

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def tree_view(self):
        data = model_to_dict(self, fields=('id', 'name'))
        data.update({'children': [model_to_dict(c, fields=('id', 'name'))
                     for c in self.category_set.all()]})
        if self.parent:
            ancestor, parents = self.parent, []
            data.update({'siblings': [model_to_dict(s, fields=('id', 'name'))
                         for s in ancestor.category_set.exclude(pk=self.pk)]})
            while ancestor:
                parents.append(model_to_dict(ancestor, fields=('id', 'name')))
                ancestor = ancestor.parent
            data.update({'parents': parents})
        else:
            data.update({'parents': [], 'siblings': []})
        return data


def create_tree(data):
    """
    Saves item with childrens recursively
    """
    saved, children = 0, []
    items = [data] if isinstance(data, dict) else data
    for item in items:
        if 'name' in item:
            parent = {'parent': Category.objects.create(
                    name=item['name'], parent=item.get('parent'))}
            saved += 1
            children.extend([{**i, **parent} for i in item.get('children', [])])
    return saved + (create_tree(children) if children else 0)
