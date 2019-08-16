$(document).ready(() => {
    console.log('loaded')
    $('input').on('keypress', ev => {
        console.log(ev)
        $('.has-error').hide();
    });
});