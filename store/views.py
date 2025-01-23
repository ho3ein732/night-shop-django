from datetime import timedelta
from django.http import JsonResponse
from .forms import ReviewForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.generic import ListView
from .models import Product, Category, ProductFeatureName, Review, FavoriteProduct, Copen, UserCopenUsage, Banner
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
from .forms import SearchForm, ContactUsForm, EmailForm
from django.db.models import Q
from cart.cart import Cart


# Create your views here.


class Index(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = super().get_queryset()
        for product in products:
            if product.discount > 0:
                product.discounted_price = product.price - (product.price * product.discount // 100)
            else:
                product.discounted_price = product.price
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['newest_product'] = Product.objects.order_by('-created')[:3]
        context['top'] = Product.objects.order_by('-sell')[:3]
        context['price'] = Product.objects.order_by('-price')[:3]
        context['off'] = Product.objects.order_by('-discount')[:3]
        context['blogs'] = BlogPost.objects.filter(status='published')
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['top_banners'] = Banner.objects.filter(status=True, position='top')
        context['middle_banners'] = Banner.objects.filter(status=True, position='middle')
        context['button_banners'] = Banner.objects.filter(status=True, position='button')
        cart = Cart(request=self.request)
        context['my_price'] = cart.get_total_price()
        return context


def product_by_category(request, category_id, slug):
    if slug == 'None':

        products = Product.objects.all()
        category = None

    else:

        category = get_object_or_404(Category, slug=slug, id=category_id)
        products = Product.objects.filter(category=category)

    # region filters

    # endregion
    categories = Category.objects.filter(parent__isnull=True)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_features = ProductFeatureName.objects.values_list('name', flat=True)

    context = {
        'products': products,
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'all_features': all_features
    }

    return render(request, 'store/by_category.html', context)


def product_detail(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id, slug=product_slug)
    reviews = Review.objects.filter(product=product)
    parent_category = product.category.parent

    if parent_category:
        related_products = Product.objects.filter(category__parent=parent_category).exclude(id=product.id)[0:4]
    else:
        related_products = Product.objects.filter(category__parent=None).exclude(id=product.id)[0:4]
    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect("store:product_detail", product_id=product.id, product_slug=product.slug)
    else:

        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'related_products': related_products
    }

    return render(request, 'store/detail.html', context)


def search(request):
    products = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            print('_' * 100)
            print(products)
            print('_' * 100)

    return render(request, 'store/search.html', {'products': products})


def add_to_favorite(request, id):
    saved = None
    product = Product.objects.get(id=id)

    if not product:
        return JsonResponse({'error': 'محصول پیدا نشد'})

    favorite = FavoriteProduct.objects.filter(user=request.user, product=product).first()
    if favorite:
        saved = False
        favorite.delete()
    else:
        FavoriteProduct.objects.create(user=request.user, product=product)

    favorite_count = FavoriteProduct.objects.filter(user=request.user).count()

    return JsonResponse({'success': True, 'saved': saved, 'favorite_count': favorite_count})


def list_favorite(request):
    user = request.user
    products = FavoriteProduct.objects.filter(user=user)
    return render(request, 'store/list_favorite.html', {'products': products})


def remove_favorite(request, id):
    if request.method == 'POST':
        favorite = get_object_or_404(FavoriteProduct, user=request.user, product_id=id)
        favorite.delete()
        favorite_count = FavoriteProduct.objects.filter(user=request.user).count()
        return JsonResponse({'success': True, 'message': 'محصول با موفقیت حذف شد', 'favorite_count': favorite_count})
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر یا کاربر احراز هویت نشده است'})


def about_us(request):
    return render(request, 'store/about_us.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            form.save()
    else:
        form = ContactUsForm()
    return render(request, 'store/about_us.html', {'form': form})


def emails(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:index')
    else:
        form = EmailForm()
    return render(request, 'partials/footer.html', {'form': form})


def apply_copen(request):
    if request.method == 'POST':
        copen_code = request.POST.get('copen_code')
        order_total = int(request.POST.get('order_total'))
        if not copen_code or not order_total:
            return JsonResponse({'success': False, 'message': 'کد منقضی شده است'})

        user = request.user
        try:
            copen = Copen.objects.get(code=copen_code, )
        except Copen.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'کد منقضی شده است'})

        if not copen:
            return JsonResponse({'success': False, 'message': 'کد منقضی شده است'})
        if copen.is_valid:
            discount = (order_total * copen.discount_percent) // 100
            total = order_total - discount

            UserCopenUsage.objects.create(
                user=user, copen=copen
            )

            return JsonResponse({
                'total32': total,
                'discount': discount,
                'success': True
            })
        else:
            return JsonResponse({'success': False, 'message': 'کد تخفیف نا معتبر است'})
    return JsonResponse({'success': False, 'message': 'کد نامعتبر است'})


