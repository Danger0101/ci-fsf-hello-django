from django.test import TestCase
from todo.models import Item

class TestViews(TestCase):
    def test_get_todo_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_list.html')

    def test_get_add_item_page(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add_item.html')

    def test_get_edit_item_page(self):
        item = Item.objects.create(name='Test To Do Item')
        response = self.client.get(f'/edit/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_item.html')

    def test_can_add_item(self):
        response = self.client.post('/add', {'name': 'Test Added Item'})
        self.assertRedirects(response, '/')
        # Double-check that the item was added
        new_item = Item.objects.get(name='Test Added Item')
        self.assertIsNotNone(new_item)

    def test_can_delete_item(self):
        item = Item.objects.create(name='Test To Do Item')
        response = self.client.post(f'/delete/{item.id}', follow=True)
        self.assertRedirects(response, '/')
        # Double-check that the item was deleted
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    def test_can_toggle_item(self):
        item = Item.objects.create(name='Test To Do Item')
        response = self.client.post(f'/toggle/{item.id}', follow=True)
        self.assertRedirects(response, '/')
        # Double-check that the item was toggled
        updated_item = Item.objects.get(id=item.id)
        self.assertNotEqual(item.done, updated_item.done)
