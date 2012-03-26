function logout()
{
    var answer = confirm("Sei sicuro di voler uscire ?");

    if (answer)
        location.href = "/user/logout";
}

// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
