$("#add-accessories").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        }
	});  


$("#edit-accessories").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        }
})