from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView


class ParamMixin:
    form_class = None
    template_name = None
    redirect_url = ''
    model = None
    context_object_key = 'object'
    key_kwargs = 'pk'
    kwargs = None
    _object = None

    def get_object(self):
        pk = self.kwargs.get(self.key_kwargs)
        return get_object_or_404(self.model, pk=pk)

    def get_redirect_url(self):
        return self.redirect_url

class CustomFormView(View, ParamMixin):

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        return kwargs

class CustomListView(TemplateView, ParamMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_key] = self.get_object()
        return context

    def get_objects(self):
        return self.model.objects.all()

class CustomDetailView(TemplateView, ParamMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_key] = self.get_object()
        return context

class CustomCreateView(View, ParamMixin):

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request=request, template_name=self.template_name, context=context)

    def get_context_data(self, **kwargs):
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = {'form': form}
        return render(request=self.request, template_name=self.template_name, context=context)

class CustomUpdateView(View, ParamMixin):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        context = self.get_context_data(form=form)
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = self.kwargs.copy()
        context[self.context_object_name] = self.object
        context.update(kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self,form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class CustomDeleteView(View, ParamMixin):
    confirm_deletion = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.confirm_deletion:
            return render(request, self.template_name, self.get_context_data())
        else:
            self.perform_delete()
            return redirect(self.get_redirect_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.perform_delete()
        return redirect(self.get_redirect_url())

    def perform_delete(self):
        self.object.delete()

    def get_context_data(self, **kwargs):
        return {self.context_object_name: self.object}