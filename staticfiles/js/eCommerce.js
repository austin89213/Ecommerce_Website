  $(document).ready(function(){
    // Contact Form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action") // /abc/


    function displaySubmitting(submitBtn, defaultText, doSubmit){
      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
      } else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
      }

    }


    contactForm.submit(function(event){
      event.preventDefault()

      var contactFormSubmitBtn = contactForm.find("[type='submit']")
      var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
      console.log(contactFormSubmitBtnTxt);


      var contactFormData = contactForm.serialize()
      var thisForm = $(this)
      displaySubmitting(contactFormSubmitBtn, "", true)
      $.ajax({
        method: contactFormMethod,
        url:  contactFormEndpoint,
        data: contactFormData,
        success: function(data){
          contactForm[0].reset()
          $.alert({
            title: "Success!",
            content: data.message,
            theme: "modern",
          })
          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
          }, 500)
        },
        error: function(error){
          console.log(error.responseJSON)
          var jsonData = error.responseJSON
          var msg = ""

          $.each(jsonData, function(key, value){ // key, value  array index / object
            msg += key + ": " + value[0].message + "<br/>"
          })

          $.alert({
            title: "Oops!",
            content: msg,
            theme: "modern",
          })

          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
          }, 500)

        }
      })
    })

    // Auto search and display searching
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") // input = name='q'
    var typingTimer
    var typingInterval = 1500 // 0.5seconds
    var searchBtn = searchForm.find("[type='submit']")
    searchInput.keyup(function(event){
      clearTimeout(typingTimer)
      typingTimer = setTimeout(performSearch,typingInterval)
    })
    searchInput.keydown(function(event){
      clearTimeout(typingTimer)
      typingTimer = setTimeout(performSearch,typingInterval)
    })

    function displaySearching() {
      searchBtn.addClass("disabled")
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch() {
      displaySearching()
      var query = searchInput.val()
      setTimeout(function(){
        window.location.href='/search/?q=' + query
},1000)
    }



    // Upadte cart and add / remove items
    var productForm = $(".form-product-ajax") // id:#form-product-ajax
    productForm.submit(function(event){
      event.preventDefault();
      console.log("Form is not sending");
      var thisForm =$(this);
      var actionEndpoint = thisForm.attr('data-endpoint');

      var httpMethod = thisForm.attr('method');
      var formData = thisForm.serialize();

      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function (data) {
          console.log("success");
          console.log(data);
          console.log("Added:",data.productAdded);
          console.log("Removed:",data.productRemoved);
          var submitSpan = thisForm.find(".submit-span")
          if (data.productAdded) {
            submitSpan.html('<button  class="btn btn-danger btn-sm "  type="submit" name="remove">Remove</button>')
          } else {
            submitSpan.html('<button  class="btn btn-success btn-sm"  type="submit" name="Add">Add to Cart</button>')
          }
          var navbarCount = $(".navbar-cart-count")
          navbarCount.text(data.cartItemCount)
          var currentPath = window.location.href
          if (currentPath.indexOf("cart") != -1) {
                 refreshCart()
             }
        },
        error: function (errorData) {
          $.alert({
            title:"Oops!",
            content:"An error occurred",
            theme:"modern"
          })
          console.log("error");
          console.log(errorData);
        }
      })
    })

    function refreshCart() {
      console.log("in current cart");
      var cartTable = $(".cart-table")
      var cartBody = cartTable.find(".cart-body")
      var productRows = cartBody.find(".cart-products")
      var currentUrl = window.location.href
      var refreshCartUrl ='api/carts'
      var refreshCartMethod="GET";
      var data={};
      $.ajax({
        url: refreshCartUrl,
        method: refreshCartMethod,
        data:data,
        success:function(data) {
          var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

          if (data.products.length>0) {
            productRows.html(" ")
            i = data.products.length
            $.each(data.products,function (index,value) {
              console.log(value);
              var newCartItemRemove = hiddenCartItemRemoveForm.clone()
              newCartItemRemove.css("display","none")
              newCartItemRemove.find(".cart-item-product-id").val(value.id)
              cartBody.prepend("<tr><th scope=\"row\">" + i +"</th><td><a href='" +value.url + "'>" + value.name +"</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
              i --
            })

            cartBody.find(".cart-subtotal").text(data.subtotal);
            cartBody.find(".cart-tax").text(data.tax);
            cartBody.find(".cart-total").text(data.total);
          }else {
            window.location.href = currentUrl;
          }
        },
        error:function(errorData) {
          console.log("error");
          console.log(errorData);
        }
      })
    }

  })
