this.ckan.module("api-info",function(o,t){return{modal:null,options:{template:null,i18n:{noTemplate:t("There is no API data to load for this resource"),loadError:t("Failed to load data API information")}},initialize:function(){o.proxyAll(this,/_on/),this.el.on("click",this._onClick),this.el.button()},loading:function(o){this.el.button(o!==!1?"loading":"reset")},show:function(){var t=this.sandbox,i=this;return this.modal?this.modal.modal("show"):void this.loadTemplate().done(function(n){i.modal=o(n),i.modal.find(".modal-header :header").append('<button class="close" data-dismiss="modal">×</button>'),i.modal.modal().appendTo(t.body)})},hide:function(){this.modal&&this.modal.modal("hide")},loadTemplate:function(){return this.options.template?(this.promise||(this.loading(),this.promise=o.get(this.options.template),this.promise.then(this._onTemplateSuccess,this._onTemplateError)),this.promise):(this.sandbox.notify(this.i18n("noTemplate")),o.Deferred().reject().promise())},_onClick:function(o){o.preventDefault(),this.show()},_onTemplateSuccess:function(){this.loading(!1)},_onTemplateError:function(){this.loading(!1),this.sandbox.notify(this.i18n("loadError"))}}});