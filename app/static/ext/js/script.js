$(document).ready(function(){

	// 点击非class=select-all的标签则添加到已选标签中
	$("#select1 dd").click(function () {
		// 将点击的dd标签增加id=selected, 并且移除同胞标签的selected
		$(this).addClass("selected").siblings().removeClass("selected");
		// 如果该标签是select-all, 则将id=selectA的标签移除
		if ($(this).hasClass("select-all")) {
			$("#selectA").remove();
		} else {
			// 否则,将该标签复制一份,
			var copyThisA = $(this).clone();
			// 如果id=selectA标签长度大于零,则将改签的html设置为选择的标签的内容
			if ($("#selectA").length > 0) {
				$("#selectA a").html($(this).text());
			// 否则,id=selectA标签长度为0,则在class=select-result的dl标签新增一个id=selectA的dd标签
			} else {
				$(".select-result dl").append(copyThisA.attr("id", "selectA"));
			}
		}
	});
	
	$("#select2 dd").click(function () {
		$(this).addClass("selected").siblings().removeClass("selected");
		if ($(this).hasClass("select-all")) {
			$("#selectB").remove();
		} else {
			var copyThisB = $(this).clone();
			if ($("#selectB").length > 0) {
				$("#selectB a").html($(this).text());
			} else {
				$(".select-result dl").append(copyThisB.attr("id", "selectB"));
			}
		}
	});
	
	$("#select3 dd").click(function () {
		$(this).addClass("selected").siblings().removeClass("selected");
		if ($(this).hasClass("select-all")) {
			$("#selectC").remove();
		} else {
			var copyThisC = $(this).clone();
			if ($("#selectC").length > 0) {
				$("#selectC a").html($(this).text());
			} else {
				$(".select-result dl").append(copyThisC.attr("id", "selectC"));
			}
		}
	});
	
	// 点击已选标签,则将已选标签移除
	// $("#selectA").bind("click", function () {
	$(document).on('click', '#selectA', function () {
		// 删除选择的标签
		$(this).remove();
		// class=selectall的标签添加class=selected, 并且移除同胞标签的selected属性
		$("#select1 .select-all").addClass("selected").siblings().removeClass("selected");
	});
	
	// $("#selectB").bind("click", function () {
    $(document).on('click', '#selectB', function () {
		$(this).remove();
		$("#select2 .select-all").addClass("selected").siblings().removeClass("selected");
	});
	
	// $("#selectC").bind("click", function () {
    $(document).on('click', '#selectC', function () {
		$(this).remove();
		$("#select3 .select-all").addClass("selected").siblings().removeClass("selected");
	});
	

	// 处理已筛选条件中,select-no的显示与隐藏
    $(document).on('click', '.select dd', function () {
		if ($(".select-result dd").length > 1) {
			$(".select-no").hide();
		} else {
			$(".select-no").show();
		}
	});



});