from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from . modules.clone_users import CloneUserAccounts #import CloneUserAccounts
from . modules import db_operations
from .modules import database, traits_female
from .models import Users
from .forms import UserForm

# @login_required
# def user_home(request):
#     # CloneUserAccounts().klone_users()
#     return render(request, 'app/home.html')
import datetime

@login_required
def generate_shows(request):
    from django.contrib import messages
    if request.method == "GET":
        from .modules import enviroments
        last_post_time_str = request.session.get('last_post_time')
        if last_post_time_str:
            last_post_time = datetime.datetime.strptime(last_post_time_str, "%Y-%m-%d %H:%M:%S.%f")
            if (datetime.datetime.now() - last_post_time).total_seconds() < 600:
                wait_time = int(600 - (datetime.datetime.now() - last_post_time).total_seconds())
                messages.warning(request, f'Please wait for {wait_time} seconds before generating another show.')
                return render(request, 'app/generate_shows.html')
        gender_id = Users.objects.get(username=request.user).gender_id
        if gender_id == 2:
            hair_style =  ['Default','hair bun','curly hair','egyptian bob hair','long_braid hair','buzzcut','dreads','side buns hair','pigtail','emo hair','knotless braid hair','updo','ponytail']
        elif gender_id == 1:
            hair_style = ['Default','hair bun','curly hair','egyptian bob hair','long_braid hair','buzzcut','dreads','baldie','emo hair','knotless braid hair','updo','ponytail']
        context = {'enviroment': enviroments.data_list, 'hair_style': hair_style}
        return render(request, 'app/generate_shows.html', context)
    else:
        import subprocess
        import threading
        
        from django.http import JsonResponse
        last_post_time_str = request.session.get('last_post_time')
        print(f'lasatposttime {last_post_time_str}')
        if last_post_time_str:
            
            last_post_time = datetime.datetime.strptime(last_post_time_str, "%Y-%m-%d %H:%M:%S.%f")
            if (datetime.datetime.now() - last_post_time).total_seconds() < 600:
                wait_time = int(600 - (datetime.datetime.now() - last_post_time).total_seconds())
                messages.warning(request, f'Please wait for {wait_time} seconds before generating another show.')
                return render(request, 'app/generate_shows.html')
                # return JsonResponse({'message': f'Please wait for {wait_time} seconds before generating another show.'})
        print('out of if ')
        # If enough time has passed or it's the first POST request, update the last_post_time in the session
        request.session['last_post_time'] = str(datetime.datetime.now())    
        environment = request.POST.get('enviroment_selectbox')
        hairstyle = request.POST.get('hairstyle_selectbox')
        if hairstyle == 'Default':
            hairstyle = 'None'
        nsfw_checkbox = request.POST.get('nsfw_checkbox')
        # Define the command as a list of strings
        if nsfw_checkbox == 'on':
            command = ["python3", "/workspace/klona/agent_generator_fashion_show.py", "--agent-handle", f"'{str(request.user)}'", "--hairstyle", f"'{hairstyle}'", "--environment", f"'{environment}'", "--nsfw"]
        else:
            command = ["python3", "/workspace/klona/agent_generator_fashion_show.py", "--agent-handle", f"'{str(request.user)}'", "--hairstyle", f"{hairstyle}", "--environment", f"{environment}"]
        # Run the command
        print(f'command {command}')
        # try:
        def run_subprocess():
            p = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
            )
            output, err = p.communicate()
        
        thread = threading.Thread(target=run_subprocess)
        thread.start()
            # print(output, err)
        # except subprocess.CalledProcessError as e:
        #     print("An error occurred:", e)
        context = {'message':f'Generating shows of {environment} with {hairstyle} hairstyle'}
        return redirect('generate_shows')

@login_required
def update_appearance(request):
    import subprocess
    import threading
    
    if request.method == 'POST':
        print(f'post request {request.POST}')
        my_traits = request.POST.get('my_traits_input')
        new_traits = request.POST.get('new_traits_input')
        user_name = str(request.user)
        command = ["python3", "/workspace/klona/agent_all_avatars.py", "--agent-handle", f"'{str(request.user)}'", " --fusion-style", f"{hairstyle}", "--environment", f"{environment}"]
        # Run the command
        print(f'command {command}')
        # try:
        def run_subprocess():
            p = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
            )
            output, err = p.communicate()
        
        thread = threading.Thread(target=run_subprocess)
        thread.start()
        return render(request, 'app/update_avator.html')
    print('get request ', request)
    avator = Users.objects.get(username = request.user).avatar or 'None'
    avator_path = 'https://img.klona.ai/' + avator
    
    context = {
        'avator': avator_path,
        'username': request.user,
        'traits': traits_female.facial_traits
    }
    return render(request, 'app/update_appearance.html', context)

@login_required
def edit_user_form(request):
    print('user ', request.user)
    user = Users.objects.get(username=request.user)  # Assuming the user is logged in and you have access to the user object
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('edit_user_form')  # Redirect to the user's profile page after saving
    else:
        form = UserForm(instance=user)
    return render(request, 'app/user_form.html', {'form': form})

@login_required
def approve_entire_post(request):
    post_id = request.POST.get('post_id')
    value = request.POST.get('checkbox_value')
    return_value = db_operations.approve_entire_post(post_id, value)
    if return_value:
        return HttpResponse("Post Approved Successfuly")
    else:
        return HttpResponse("Error Occured while Approving post")

@login_required    
def update_checkbox(request):
    file_name = request.POST.get('file_name')
    value = request.POST.get('checkbox_value')
    return_value = db_operations.update_checkbox_value(file_name, value, 'nsfw')
    if return_value:
        return HttpResponse('Updated Succesfuly')
    else:
        return HttpResponse('Error occured while updating')

@login_required
def update_approve(request):
    file_name = request.POST.get('file_name')
    value = request.POST.get('checkbox_value')
    return_value = db_operations.update_checkbox_value(file_name, value, 'approved')
    if return_value:
        return HttpResponse('Updated Succesfuly')
    else:
        return HttpResponse('Error occured while updating')

@login_required
def user_home(request):
    user = str(request.user)
    # CloneUserAccounts().klone_users()
    # post_id = request.GET.get('post_id')
    post_option = request.GET.get('post_option')
    page = int(request.GET.get('page', 1))
    items_per_page = 100
    offset = (page - 1) * items_per_page
    if post_option == "approved":
        query = """
            SELECT 
            u.username,p.user_id, p.id, a.approved, a.nsfw, a.filename
            FROM 
                posts p
            LEFT JOIN 
                attachments a ON p.id = a.post_id
            LEFT JOIN 
                users u ON p.user_id = u.id
            WHERE (a.filename IS NOT NULL) AND a.approved=1 AND (a.type='png' OR a.type='jpg') AND (u.username=%s) AND (a.nsfw != 1)
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT %s OFFSET %s
            """
    elif post_option=='disapproved':
        query="""
        SELECT 
            u.username,p.user_id, p.id, a.approved, a.nsfw, a.filename
            FROM 
                posts p
            LEFT JOIN 
                attachments a ON p.id = a.post_id
            LEFT JOIN 
                users u ON p.user_id = u.id
            WHERE (a.filename IS NOT NULL) AND a.approved=-1 AND (a.type='png' OR a.type='jpg') AND (u.username=%s) AND (a.nsfw != 1)
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT %s OFFSET %s
        """
    else:
        query = """
            SELECT 
            u.username,p.user_id, p.id, a.approved, a.nsfw, a.filename
            FROM 
                posts p
            LEFT JOIN 
                attachments a ON p.id = a.post_id
            LEFT JOIN 
                users u ON p.user_id = u.id
            WHERE (a.filename IS NOT NULL) AND (a.approved IS NULL OR a.approved=0) AND (a.type='png' OR a.type='jpg') AND (u.username=%s) AND (a.nsfw != 1)
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT %s OFFSET %s
        """
    # print(f'query \n', query)
    connection = database.get_mysql_connection()
    cursor = connection.cursor()
    # with connection.cursor() as cursor:
    cursor.execute(query, (user, items_per_page, offset))
    results = cursor.fetchall()

    keys = [
        'user_name','user_id','id', 'approved', 'nsfw', 'filename'
    ]

    data = []
    current_post_id = None
    current_post_data = []

    for row in results:
        row_dict = dict(zip(keys, row))
        if row_dict['id'] != current_post_id:
            if current_post_data:
                data.append(current_post_data)
            current_post_id = row_dict['id']
            current_post_data = [row_dict]
        else:
            current_post_data.append(row_dict)

    if current_post_data:
        data.append(current_post_data)

    context = {
        'results': data,
        'next_page': page + 1,
        'post_option': post_option
    }
    # print('see here')
    # print(context['results'])
    return render(request, 'app/grid.html', context)

@login_required
def delete_image(request):
    if request.method == 'POST':
        print('in delete image function')
        file_path = 'https://img.klona.ai/'+request.POST.get('file_path')
        if file_path:
            # db_operations.delete_row(file_path)
            if db_operations.disapprove_row(file_path):
                return HttpResponse("Disapproved Image")
            else:
                return HttpResponse('Error occured while disapproving')
            # if s3_operations.delete_from_s3(file_path):
            #     return HttpResponse('Deleted Image successfully')
            # else:
            #     return HttpResponse('Error occured while Deletion')
    # Handle invalid or unauthorized requests here if needed
    return redirect('get_data')  # Redirect to grid view if the request is not a valid POST
