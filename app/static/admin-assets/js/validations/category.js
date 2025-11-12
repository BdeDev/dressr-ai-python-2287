$("#add-cloth-category").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
        icon: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        },
        icon: {
			required: "Please upload icon",
            accept: "jpg,png,jpeg,svg",
			},
	});  


$("#edit-cloth-category").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
        icon: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
		},
        icon: {
			required: "Please upload icon",
            accept: "jpg,png,jpeg,svg",
			},
})