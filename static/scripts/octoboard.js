var Repo = Backbone.Model.extend({
	initialize: function () {
	}
});


var RepoCollection = Backbone.Collection.extend({
	model: Repo,
	url: '/api?path=/user/repos%3Fper_page%3D100'
});


var RepoView = Backbone.View.extend({
	tagName: 'li',
	className: 'repo',
	events: {},
	render: function () {
		this.$el.html(this.model.get('name'));
		return this;
	}
});


var RepoList = Backbone.View.extend({
	initialize: function () {
		_.bindAll(this, 'addOne');
		this.repos = new RepoCollection()
		this.repos.on('add', this.addOne, this);
		this.repos.on('reset', this.addAll, this);
		this.repos.on('all', this.render, this);

		this.repos.fetch();
	},
	events: {},
	addOne: function (repo) {
		var view = new RepoView({model: repo});
		this.$el.append(view.render().el);
	},
	addAll: function () {
		this.repos.each(this.addOne);
	},
	render: function () {
		this.$el.append('<ul id="repo_list" />');
	}
});


Zepto(function ($) {
	window.repoList = new RepoList({el: $('#my_repos')[0]});
});
