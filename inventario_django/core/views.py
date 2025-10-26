from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Gestoria, Mueble
from .forms import GestoriaForm, MuebleForm

@login_required
def home(request):
    if request.user.is_superuser:
        gestorias = Gestoria.objects.all()
    else:
        gestorias = Gestoria.objects.filter(responsable=request.user)
    return render(request, 'core/home.html', {'gestorias': gestorias})

# Crear Gestoría
@login_required
def crear_gestoria(request):
    if request.method == 'POST':
        form = GestoriaForm(request.POST)
        if form.is_valid():
            gestoria = form.save(commit=False)
            gestoria.responsable = request.user
            gestoria.save()
            return redirect('home')
    else:
        form = GestoriaForm()
    return render(request, 'core/gestoria_form.html', {'form': form, 'titulo': 'Nueva Gestoría'})

# Editar Gestoría
@login_required
def editar_gestoria(request, id):
    gestoria = get_object_or_404(Gestoria, id=id, responsable=request.user)
    if request.method == 'POST':
        form = GestoriaForm(request.POST, instance=gestoria)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GestoriaForm(instance=gestoria)
    return render(request, 'core/gestoria_form.html', {'form': form, 'titulo': 'Editar Gestoría'})

# Eliminar Gestoría
@login_required
def eliminar_gestoria(request, id):
    gestoria = get_object_or_404(Gestoria, id=id, responsable=request.user)
    if request.method == 'POST':
        gestoria.delete()
        return redirect('home')
    # Solo se envía 'gestoria' al contexto
    return render(request, 'core/gestoria_eliminar.html', {'gestoria': gestoria})

# Listado de muebles por gestoría
@login_required
def muebles_por_gestoria(request, id):
    gestoria = get_object_or_404(Gestoria, id=id, responsable=request.user)
    muebles = Mueble.objects.filter(gestoria=gestoria)
    return render(request, 'core/muebles.html', {'gestoria': gestoria, 'muebles': muebles})

# Agregar mueble
@login_required
def agregar_mueble(request, id):
    gestoria = get_object_or_404(Gestoria, id=id, responsable=request.user)
    if request.method == 'POST':
        form = MuebleForm(request.POST)
        if form.is_valid():
            mueble = form.save(commit=False)
            mueble.gestoria = gestoria
            mueble.save()
            return redirect('muebles_por_gestoria', id=gestoria.id)
    else:
        form = MuebleForm()
    return render(request, 'core/mueble_form.html', {'form': form, 'titulo': 'Nuevo Mueble', 'gestoria': gestoria})

# Editar mueble
@login_required
def editar_mueble(request, id):
    mueble = get_object_or_404(Mueble, id=id, gestoria__responsable=request.user)
    if request.method == 'POST':
        form = MuebleForm(request.POST, instance=mueble)
        if form.is_valid():
            form.save()
            return redirect('muebles_por_gestoria', id=mueble.gestoria.id)
    else:
        form = MuebleForm(instance=mueble)
    return render(request, 'core/mueble_form.html', {'form': form, 'titulo': 'Editar Mueble', 'gestoria': mueble.gestoria})

# Eliminar mueble
@login_required
def eliminar_mueble(request, id):
    mueble = get_object_or_404(Mueble, id=id, gestoria__responsable=request.user)
    if request.method == 'POST':
        gestoria_id = mueble.gestoria.id
        mueble.delete()
        return redirect('muebles_por_gestoria', id=gestoria_id)
    return render(request, 'core/mueble_eliminar.html', {'mueble': mueble})