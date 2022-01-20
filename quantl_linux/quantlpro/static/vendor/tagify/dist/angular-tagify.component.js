"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TagifyComponent = void 0;
const core_1 = require("@angular/core");
let TagifyComponent = class TagifyComponent {
    constructor(tagifyService) {
        this.tagifyService = tagifyService;
        this.add = new core_1.EventEmitter(); // returns the added tag + updated tags list
        this.remove = new core_1.EventEmitter(); // returns the updated tags list
    }
    ngAfterViewInit() {
        if (!this.settings)
            return;
        this.settings.callbacks = {
            add: () => this.add.emit({
                tags: this.tagify.value,
                added: this.tagify.value[this.tagify.value.length - 1]
            }),
            remove: () => this.remove.emit(this.tagify.value)
        };
        this.tagify = this.tagifyService.getTagifyRef(this.tagifyInputRef.nativeElement, this.settings);
    }
};
__decorate([
    (0, core_1.Output)()
], TagifyComponent.prototype, "add", void 0);
__decorate([
    (0, core_1.Output)()
], TagifyComponent.prototype, "remove", void 0);
__decorate([
    (0, core_1.Input)()
], TagifyComponent.prototype, "settings", void 0);
__decorate([
    (0, core_1.ViewChild)('tagifyInputRef')
], TagifyComponent.prototype, "tagifyInputRef", void 0);
TagifyComponent = __decorate([
    (0, core_1.Component)({
        selector: 'tagify',
        template: `<input *ngIf="settings" #tagifyInputRef/>`
    })
], TagifyComponent);
exports.TagifyComponent = TagifyComponent;
