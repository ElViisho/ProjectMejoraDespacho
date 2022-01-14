function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

$('.Estado').change(function () {
    var url = window.location.href;
    var option = $(this).val();
    var nvv = this.id;

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        success: function () {
            $.post(url, {"option": option, "nvv": nvv});
        }
    })

    
})

$(document).ready(function() {
    document.getElementById('filtro_NVV').style.width = "20%";
    $('#filtro_NVV').select2();
    document.getElementById('filtro_region').style.width = "20%";
    $('#filtro_region').select2();
    document.getElementById('filtro_comuna').style.width = "20%";
    $('#filtro_comuna').select2();
});


$("#filtro_region").change(function () {
    var url = "ajax/load-comunas/";
    var regionId = $(this).val();

    $.ajax({
        url: url,
        data: {
            'region': regionId
        },
        success: function (data) {
            if (regionId == 0) {
                $("#filtro_comuna").prop('disabled', true);
                $("#filtro_comuna").html("<option value=0>---------------</option>")
            }
            else {
                $("#filtro_comuna").prop('disabled', false);
                $("#filtro_comuna").html("<option value=0>---------------</option>")
                $("#filtro_comuna").append(data);
            }
        }
    });
});