this.ckan.module("slug-preview-target",{initialize:function(){var e=this.sandbox,i=(this.options,this.el);e.subscribe("slug-preview-created",function(e){i.after(e)}),""==i.val()&&(e.subscribe("slug-preview-modified",function(){i.off(".slug-preview")}),i.on("keyup.slug-preview",function(i){e.publish("slug-target-changed",this.value)}))}}),this.ckan.module("slug-preview-slug",function(e,i){return{options:{prefix:"",placeholder:"<slug>",i18n:{url:i("URL"),edit:i("Edit")}},initialize:function(){var i,s=this.sandbox,t=this.options,n=this.el,r=(s.translate,n.slug()),l=r.parents(".control-group");l.length&&(l.hasClass("error")||(i=l.slugPreview({prefix:t.prefix,placeholder:t.placeholder,i18n:{URL:this.i18n("url"),Edit:this.i18n("edit")}}),r.keypress(function(){event.charCode&&s.publish("slug-preview-modified",i[0])}),s.publish("slug-preview-created",i[0]),e("html").hasClass("ie7")&&(e(".btn").on("click",i,function(){e(".controls").ie7redraw()}),i.hide(),setTimeout(function(){i.show(),e(".controls").ie7redraw()},10))),s.subscribe("slug-target-changed",function(e){r.val(e).trigger("change")}))}}});