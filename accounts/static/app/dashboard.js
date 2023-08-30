function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    // console.log("in if");
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
          console.log("in nested if");
        cookieValue = cookie.substring(name.length + 1);
        break;
      }
    }
  }
  return cookieValue;
}

// const csrfToken = getCookie('csrftoken');
// console.log('csrf token '+csrfToken);

function submitForm() {
    // Get the form containing the select element
    var form = document.getElementById("postForm");

    // Submit the form
    form.submit();
}

function ApproveEntirePost(postid){
    let checkbox = document.getElementById(postid);
    let checkboxValue = checkbox.checked ? 1:0;
    console.log('entire post checkbox value '+checkboxValue);
    $.ajax({
        url:'/app/approve_entire_post/',
        type: 'POST',
        data: {checkbox_value: checkboxValue, post_id: postid},
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (response){
            alert('message: ' + response + ' ' + checkboxValue);
            console.log(response);
        },
        error: function(xhr, status, error) {
          // Handle the error response from the backend
          alert('Unable to Approve Entire Post: ' + error);
          console.log('message ', error);
          // Add any additional error handling code as needed
        }
    })
}

function handleApprove(filename) {
      let checkbox = document.getElementsByName(filename);
      let checkboxValue = checkbox[0].checked ? 1 : 0;
      console.log(checkboxValue);
    
      $.ajax({
        url: '/app/update_approve/',
        type: 'POST',
        data: { checkbox_value: checkboxValue, file_name: filename },
        beforeSend: function(xhr, settings){
          xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
      },
        success: function(response) {
          // Handle the success response from the backend
          alert('message: ' + response + ' ' + checkboxValue);
          console.log(response);
          // Add any additional code you want to execute after a successful update
        },
        error: function(xhr, status, error) {
          // Handle the error response from the backend
          alert('Unable to update: ' + error);
          console.log('message ', error);
          // Add any additional error handling code as needed
        }
      });
}
// nsfw checkbox
function handleNsfw(id) {
    let checkbox = document.getElementById(id);
    let checkboxValue = checkbox.checked ? 1 : 0;
    console.log("Checkbox value: " + checkboxValue);
    // You can use the checkboxValue variable as needed (e.g., send it to a server, perform calculations, etc.)
    $.ajax({
        url: '/app/update_checkbox/',
        type: 'POST',
        data: { checkbox_value: checkboxValue, file_name:id },
        beforeSend: function(xhr, settings) {
            // Set the CSRF token in the AJAX request headers
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success: function(response) {
            // Handle the success response from the backend
            // checkbox.style.color= 'green';
        //   console.log("id "+id);
          let label = document.querySelector('label[for="' + id + '"]');
          if(checkboxValue==1){
            label.style.color = 'green';
          }
          else{
            label.style.color='black';
          }
          
            // checkbox.classList.add('success-color');
            // alert('message: '+ response+' '+checkboxValue);
            console.log(response);
        },
        error: function(xhr, status, error) {
            // Handle the error response from the backend
            alert('Unable to update: ' + error);
            console.log('message ', error);
        }
    });
}

function deleteFromS3(file_path) {
    
    // Make an AJAX request to a Python backend to delete the image from S3
    $.ajax({
        url: '/app/delete_image/',
        type: 'POST',
        data: { file_path: file_path },
        beforeSend: function(xhr, settings) {
            // Set the CSRF token in the AJAX request headers
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success: function(response) {
            // Handle the success response from the backend
            alert('Message: '+response);
            console.log(response);
            // Add any additional code you want to execute after successful deletion
        },
        error: function(xhr, status, error) {
            // Handle the error response from the backend
            alert('Unable to delete: ' + error);
            console.log(error);
            // Add any additional error handling code as needed
        }
    });
}

// Function to retrieve the CSRF token value from the cookie


function deleteImage(filepath) {
    // Add code here to handle the delete action
    // For example, you can make an AJAX request to delete the image
    deleteFromS3(filepath);
}
document.addEventListener('DOMContentLoaded', function() {
    var nextPageButtons = document.querySelectorAll('.next-button button a');
    // let nextPageButtons = document.getElementById("next_page_btn");
    nextPageButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let postOption = document.querySelector('select[name="post_option"]').value;
            window.location.href = this.href + '&post_option=' + postOption;
        });
    });
});