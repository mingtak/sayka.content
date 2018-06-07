$(document).ready(function () {
    $('.invoice_three').click(function(){
        $('.invoice_code').removeClass('hidden');
    })
    $('.invoice_two').click(function (e) { 
        $('.invoice_code').addClass('hidden');
    });
 //   $('#buyer_city').val($('#buyer_city').data('default'));
//    $('#buyer_district').val($('#buyer_district').data('default'));

    $('#buyer_city, #receiver_city, #invoice_city').change(function (e) { 
        address = $(this).val()
        target = $(this).siblings()[0]
        updateDist(address, target)
    });
    $('#buyer_district, #receiver_district, #invoice_district').change(function (e) {
        address = $(this).val()
        val = $(`option[value="${address}"]`).data('district')
        $(this).parent().find('input[type="number"]').val(val)
    });
    $('.same_with_buyer').click(function (e) {
        if($(this).prop('checked')){
        city = $('#buyer_city').val()
        district = $('#buyer_district').val()
        district_children = $('#buyer_district').children().clone()
        zip = $('#buyer_zip').val()
        buyer_address = $('#buyer_address').val()
        buyer_name = $('#buyer_name').val()
        buyer_email = $('#buyer_email').val()
        buyer_phoneNo = $('#buyer_phoneNo').val()
        buyer_cellNo = $('#buyer_cellNo').val()
        if($(this).data('same') == 'receiver'){
            $('#receiver_district').html('')
            $('#receiver_city').val(city)
            $('#receiver_district').append(district_children)
            $('#receiver_district').val(district)
            $('#receiver_zip').val(zip)
            $('#receiver_address').val(buyer_address)
            $('#receiver_name').val(buyer_name)
            $('#receiver_phoneNo').val(buyer_phoneNo)
            $('#receiver_cellNo').val(buyer_cellNo)
            $('#receiver_email').val(buyer_email)
        }else{
            $('#invoice_district').html('')
            $('#invoice_city').val(city)
            $('#invoice_district').append(district_children)
            $('#invoice_district').val(district)
            $('#invoice_zip').val(zip)
            $('#invoice_address').val(buyer_address)
        }
      }
    });
    $('#receiver').change(function (e) { 
        receiver_name = $(this).val()
        data = $(this).find(`option[data-key=${receiver_name}]`).data()
        name = data['name']
        city = data['city']
        zip = data['zip']
        phoneNo = data['phoneno']
        cellNo = data['cellno']
        district = data['district']
        address = data['address']
        email = data['email']
        $('#receiver_name').val(name)
        $('#receiver_phoneNo').val(phoneNo)
        $('#receiver_cellNo').val(cellNo)
        $('#receiver_city').val(city)
        $('#receiver_zip').val(zip)
        $('#receiver_email').val(email)
        $('#receiver_address').val(address)
        target = $('#receiver_district')
        updateDist(city, target, district)
    });
    $('#invoice').change(function (e) { 
        invoice_name = $(this).val()
        data = $(this).find(`option[data-key=${invoice_name}]`).data()
        name = data['name']
        city = data['city']
        zip = data['zip']
        code = data['code']
        district = data['district']
        address = data['address']
        $('#invoice_name').val(name)
        $('#invoice_code').val(code)
        $('#invoice_city').val(city)
        $('#invoice_zip').val(zip)
        $('#invoice_district').val(district)
        $('#invoice_address').val(address)
        target = $('#invoice_district')
        updateDist(city, target, district)
    });

});


updateDist = function(address, target, district = ''){
    url = window.location.href.replace('billing', 'update_dist')
    data = {
        'address':address
    }
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (response) {
            $(target).empty()
            obj_res = JSON.parse(response)
            $(target).append('<option>請選擇縣市</option>')
            for(k in obj_res){
                $(target).append(`<option value="${k}" data-district="${obj_res[k]}">${k}</option>`)
            }
            if (district == ''){
                $(target).val('請選擇縣市')
            }else{
                $(target).val(district)            
            }
        }
    });
}
