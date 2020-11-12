from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic.edit import DeleteView, CreateView
from django.views.generic import View, ListView 

from django.forms import inlineformset_factory

from .models import Form, Field

class FormListView(ListView):
    model = Form
    context_object_name = 'forms'

class FormDeleteView(DeleteView):
    model = Form
    
def FormCreateView(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        f = Form(user=request.user, name=request.POST.get('name'))
        f.save()
        return redirect(f)

class FormView(View):
    
    FieldFormSet = inlineformset_factory(Form, Field, fields=('name',), extra=1)

    def get(self, request, pk=None):
        ctx = {
            'form':Form.objects.get(id=pk)
        }
        ctx['formset'] = self.FieldFormSet(instance=ctx['form'])
        return render(request, 'form_generator/form_create.html', ctx)
    
    def post(self, request, pk):
        instance = Form.objects.get(id=pk)
        form = self.FieldFormSet(request.POST, instance=instance)
        if form.is_valid():
            i = form.save()
            return redirect(instance.get_absolute_url())
             
class FormFillView(View):
    def get(self):
        return render(self.request, 'form_generator/form_generator.html')

