from django.shortcuts import render

from .models import Book, Author, BookInstance, Genre

def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',  # [[if you created template\catalog\index.html, then use catalog\index.html]]
        context={'num_books':num_books,
                 'num_instances':num_instances,                
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors, 
                 'num_visits':num_visits}, 
    )

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    # book_list = Book.objects.all()
    # return render(request, 'catalog/book_list.html', context={'book_list':book_list} )

class BookDetailView(generic.DetailView):
    model = Book
    # def book_detail_view(request,pk):
    #     book_id=get_object_or_404(Book, pk=pk)
    #     return render(request, 'catalog/book_detail.html', context={'book':book_id,} ) 

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
class AuthorDetailView(generic.DetailView):
    model = Author

# The two views above are the same as the two below. 

# from django.shortcuts import get_object_or_404
# from django.core.paginator import Paginator, EmptyPage,  PageNotAnInteger
# def authorListView(request):
#     author_list = Author.objects.all()
#     paginator = Paginator(author_list, 2)
#     page = request.GET.get('page')
#     try:
#         author_list = paginator.page(page)      # assigns a Page object 
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         author_list = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         author_list = paginator.page(paginator.num_pages)
#     return render(request, 
#                   'catalog/author_list.html', 
#                   context={'author_list':author_list} )

# def authorDetailView(request, pk):
#     author = get_object_or_404(Author, pk=pk)
#     return render(request, 'catalog/author_detail.html', context={'author':author}) 

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)\
               .filter(status__exact='o').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin
class AllBorrowedListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned' 
    model = BookInstance
    template_name ='catalog/all_borrowed.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm
@permission_required('catalog.can_mark_returned')  
### [[ You may use  @staff_member_required  with an additional import]]       
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed') )
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
    return render(request, 'catalog/book_renew_librarian.html', 
                  {'form': form, 'bookinst':book_inst})


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.contrib.auth.mixins import PermissionRequiredMixin 

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}
    permission_required = 'is_staff'               

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
