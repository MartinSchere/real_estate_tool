from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic import View, ListView

from django.forms import inlineformset_factory

from .models import Form, Field, Submission
from .forms import FormCreate, CustomForm


class FormListView(ListView):
    model = Form
    context_object_name = 'forms'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FormCreate()
        return context


class FormDeleteView(DeleteView):
    model = Form
    success_url = reverse_lazy('form_generator')

    def get(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class FieldDeleteView(DeleteView):
    model = Field
    success_url = reverse_lazy('form_generator')

    def get(self, *args, **kwargs):
        return super().post(*args, **kwargs)


@login_required
def FormCreateView(request):
    if request.method == 'POST':
        form = FormCreate(request.POST)
        if form.is_valid():
            f = Form(user=request.user, name=form.cleaned_data.get('name'))
            f.save()
            messages.success(request, "Form has been created successfully")
            return redirect(f)
        else:
            messages.warning(request, "Form couldn't be created")
            return redirect('form_generator')


class FormView(View):
    FieldFormSet = inlineformset_factory(
        Form, Field, fields=('question',), extra=1, can_delete=False)

    def get(self, request, pk=None):
        ctx = {
            'form': Form.objects.get(id=pk)
        }
        ctx['formset'] = self.FieldFormSet(instance=ctx['form'])
        return render(request, 'form_generator/form_create.html', ctx)

    def post(self, request, pk):
        instance = Form.objects.get(id=pk)
        form = self.FieldFormSet(request.POST, instance=instance)
        if form.is_valid():
            i = form.save()
            return redirect(instance.get_absolute_url())
        return redirect(reverse_lazy('form_generator'))


def ThanksView(request):
    return render(request, 'form_generator/thanks.html')


class FormFillView(View):

    def get(self, request, pk):
        form = Form.objects.get(pk=pk)
        return render(self.request, 'form_generator/form.html', {'form': form})

    def post(self, request, pk):
        f = Form.objects.get(pk=pk)
        form = f.applicant_form(request.POST)
        if form.is_valid():
            submission = Submission.objects.create(
                form=f, data=form.cleaned_data)
            return redirect('thanks')
