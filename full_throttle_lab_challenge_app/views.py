from django.shortcuts import render
from rest_framework.views import APIView, Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

# Create your views here.
def home(request):
   return render(request, 'full_throttle_lab_challenge_app/user_input.html')

def takeFirst(elem):
    return list(elem.keys())[0]

@csrf_exempt
@api_view(['GET'])
def find_matched_words(request):
    if request.GET.get('word'):
        to_find = request.GET['word']
        tsv_file = open('./full_throttle_lab_challenge_app/static/full_throttle_lab_challenge_app/word_search.tsv','r').read().split('\n')
        find_list = []
        tsv_file.pop(len(tsv_file)-1)
        for words in tsv_file:
            word_fre = words.split('\t')
            word = word_fre[0]
            frequency = word_fre[1]
            matched_word_index = word.find(to_find)
            if matched_word_index >= 0:
                if matched_word_index in [list(list_item.keys())[0] for list_item in find_list]:
                    find_list[[list(list_item.keys())[0] for list_item in find_list].index(matched_word_index)][matched_word_index].append({int(frequency):word})
                    pass
                else:
                    find_list.append({matched_word_index:[{int(frequency):word}]})

        find_list = sorted(find_list, key=takeFirst)
        sorted_find_list = []
        for list_items in find_list:
            sorted_find_list.append({list(list_items.keys())[0] : sorted(list_items[list(list_items.keys())[0]], key=takeFirst, reverse=True)})

        list_to_return = []
        for sorted_item in sorted_find_list:
            list_to_return.extend(sorted_item[list(sorted_item.keys())[0]])
        
        # print(list_to_return)
        list_to_return = [list(i.values())[0] for i in list_to_return][:25]
        # print(response_to_return)

        return Response({'status' : 200,'result' : list_to_return})
    else:
        return Response({'status' : 400, 'result' : 'Please insert a valid word!'})
