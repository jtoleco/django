from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from polls.models import Choice, Question, Item
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

"""
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
"""
from openpyxl import Workbook

class IndexView(generic.ListView):
    print('Index View')
    workbook = Workbook()
    sheet = workbook.active

    sheet["A1"] = "hello"
    sheet["B1"] = "world!"

    workbook.save(filename="hello_world.xlsx")
    
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def ajax(request):
    item = Item.objects.get(pk=1)  # Replace 1 with the actual ID of the item you want to pass
    context = {
        'item': item,
    }
    return render(request, 'polls/ajax.html', context)
    
    
@csrf_exempt
def update_item(request):
  print(f'update_item view def')
  if request.method == "POST":
    item_id = request.POST.get('item_id')
    new_value = request.POST.get('new_value')
    
    print(f'item_id: {item_id} new_value: {new_value}')

    try:
      item = get_object_or_404(Item, pk=item_id)
      item.value = new_value
      item.save()

      return JsonResponse({'new_value': new_value})
    except Item.DoesNotExist:
      return JsonResponse({'error': 'Item not found'}, status=404)

  return JsonResponse({'error': 'Invalid request'}, status=400)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))