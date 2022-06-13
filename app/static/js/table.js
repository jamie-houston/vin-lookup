var $table = $('#table'),
    selections = [];

function initTable() {

// sometimes footer render error.
    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);


    $table.on('all.bs.table', function (e, name, args) {
        console.log(name, args);
    });

    $(window).resize(function () {
        $table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
}


function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}

$(function () {
    initTable();
});
