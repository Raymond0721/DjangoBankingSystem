from django.views.generic import ListView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import Bank, Branch
from .forms import BankForm, BranchForm
from functools import wraps
from django.core.validators import EmailValidator
from django.forms import model_to_dict
from django.urls import reverse
from django.utils import timezone


def auth_check(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@auth_check
def BankCreateView(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        bank = form.save(request.user)
        if bank is not None:
            return redirect(reverse('bank_detail', args=[bank.bank_id]))
    else:
        form = BankForm()

    return render(request, 'banks/bank.html', {'form': form})


@auth_check
def BranchCreateView(request, bank_id):
    bank = get_object_or_404(pk=bank_id, klass=Bank)
    if bank.owner != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        add_branch_form = BranchForm(request.POST)
        if add_branch_form.is_valid():
            branch = add_branch_form.save(request.user, bank)
            if branch is not None:
                return redirect(reverse('branch_detail', args=[branch.branch_id]))
    else:
        add_branch_form = BranchForm(initial={'email': 'admin@utoronto.ca'})

    return render(request, 'banks/create.html', {'form': add_branch_form, 'bank_id': bank_id})


def BranchDetailView(request, branch_id):
    branch = get_object_or_404(pk=branch_id, klass=Branch)
    return JsonResponse({
        'id': branch.branch_id,
        'name': branch.name,
        'transit_num': branch.transit_num,
        'address': branch.address,
        'email': branch.email,
        'capacity': branch.capacity,
        'last_modified': branch.last_modified,
    })


def BranchListView(request, bank_id):
    bank = get_object_or_404(pk=bank_id, klass=Bank)
    branches = bank.branches.all()

    branches_list = []
    for branch in branches:
        print(f"branch: {branch.last_modified}")
        branch_dict = model_to_dict(branch)
        branch_dict['id'] = branch_dict.pop('branch_id', None)
        branch_dict.pop('bank', None)
        branch_dict['last_modified'] = branch.last_modified
        branches_list.append(branch_dict)

    return JsonResponse(branches_list, safe=False)


class BranchUpdateView(UpdateView):
    model = Branch
    template_name = 'banks/edit_branch.html'
    fields = ['name', 'transit_num', 'address', 'email', 'capacity']
    pk_url_kwarg = 'branch_id'

    def get_success_url(self):
        return reverse('branch details', kwargs={'branch_id': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        branch = self.get_object()
        if branch.bank.owner != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        email_validator = EmailValidator()
        form.fields['email'].validators.append(email_validator)
        form.instance.last_modified = timezone.now()
        return form


class BankListView(ListView):
    model = Bank
    template_name = 'banks/list.html'
    context_object_name = 'banks'

    def get_queryset(self):
        return Bank.objects.all()


def BankDetailView(request, bank_id):
    bank = get_object_or_404(pk=bank_id, klass=Bank)
    return render(request, 'banks/detail.html', {'bank': bank})
