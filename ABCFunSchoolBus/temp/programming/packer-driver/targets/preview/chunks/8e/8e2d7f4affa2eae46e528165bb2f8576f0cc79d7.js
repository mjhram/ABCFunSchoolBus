System.register(["cc"], function (_export, _context) {
  "use strict";

  var _cclegacy, __checkObsolete__, __checkObsoleteInNamespace__, _decorator, Component, Node, Sprite, SpriteFrame, UITransform, Graphics, Color, Label, UIOpacity, Vec3, tween, resources, input, Input, KeyCode, view, ResolutionPolicy, Canvas, Camera, Layers, ImageAsset, Texture2D, sys, _dec, _class, _crd, ccclass, W, H, HOR, CAM_H, F, ROAD_HALF, BUS_LIM, ACCEL, BRAKE_DECEL, STEER_SPEED, SPAWN_Z, COLLECT_Z, LETTER_CY, FONT, SAVE_KEY, LETTERS, FILES, C, shade, shadeHex, THEMES, LEVELS, GameMain;

  return {
    setters: [function (_cc) {
      _cclegacy = _cc.cclegacy;
      __checkObsolete__ = _cc.__checkObsolete__;
      __checkObsoleteInNamespace__ = _cc.__checkObsoleteInNamespace__;
      _decorator = _cc._decorator;
      Component = _cc.Component;
      Node = _cc.Node;
      Sprite = _cc.Sprite;
      SpriteFrame = _cc.SpriteFrame;
      UITransform = _cc.UITransform;
      Graphics = _cc.Graphics;
      Color = _cc.Color;
      Label = _cc.Label;
      UIOpacity = _cc.UIOpacity;
      Vec3 = _cc.Vec3;
      tween = _cc.tween;
      resources = _cc.resources;
      input = _cc.input;
      Input = _cc.Input;
      KeyCode = _cc.KeyCode;
      view = _cc.view;
      ResolutionPolicy = _cc.ResolutionPolicy;
      Canvas = _cc.Canvas;
      Camera = _cc.Camera;
      Layers = _cc.Layers;
      ImageAsset = _cc.ImageAsset;
      Texture2D = _cc.Texture2D;
      sys = _cc.sys;
    }],
    execute: function () {
      _crd = true;

      _cclegacy._RF.push({}, "7c1d2oQO05PWoydDh8qO0xd", "GameMain", undefined);

      __checkObsolete__(['_decorator', 'Component', 'Node', 'Sprite', 'SpriteFrame', 'UITransform', 'Graphics', 'Color', 'Label', 'UIOpacity', 'Vec3', 'tween', 'resources', 'input', 'Input', 'EventKeyboard', 'KeyCode', 'view', 'ResolutionPolicy', 'Canvas', 'Camera', 'Layers', 'ImageAsset', 'Texture2D', 'sys']);

      ({
        ccclass
      } = _decorator);
      /**
       * ABC Fun School Bus  -  2.5D (pseudo-3D perspective) multi-level learning game.
       * Design resolution 1280x720 (16:9, landscape).
       *
       * World model: the bus sits at z = 0 and drives "into" the screen.
       *   screenX = (x - busX) * F / z      screenY = HORIZON - CAM_H * F / z
       * Sprites are scaled by F / z, so they grow as they approach.
       */
      // ---------------------------------------------------------------- constants

      W = 1280;
      H = 720;
      HOR = 40;
      CAM_H = 1.2;
      F = 620;
      ROAD_HALF = 3.2;
      BUS_LIM = 1.9;
      ACCEL = 4;
      BRAKE_DECEL = 12;
      STEER_SPEED = 2.6;
      SPAWN_Z = 70;
      COLLECT_Z = 2.2;
      LETTER_CY = 140;
      FONT = "'Arial Rounded MT Bold','Comic Sans MS','Trebuchet MS',Arial";
      SAVE_KEY = 'abc_fun_school_bus_v2';
      LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(ch => 'letter_' + ch);
      FILES = [...LETTERS, 'button_arrow_left', 'button_arrow_right', 'button_brake', 'button_brake_pressed', 'button_horn', 'button_horn_pressed', 'dashboard', 'mascot_puppy', 'progressbar_frame', 'rearview_mirror', 'scenery_houses', 'scenery_trees', 'speech_bubble', 'speedometer', 'star_golden', 'steering_wheel', 'traffic_ice_cream_van', 'vfx_smoke_puff', 'vfx_star_burst'];

      C = function C(hex, a) {
        if (a === void 0) {
          a = 255;
        }

        var n = parseInt(hex.slice(1), 16);
        return new Color(n >> 16 & 255, n >> 8 & 255, n & 255, a);
      };

      shade = function shade(hex, f, a) {
        if (a === void 0) {
          a = 255;
        }

        var n = parseInt(hex.slice(1), 16);

        var cl = v => Math.max(0, Math.min(255, Math.round(v * f)));

        return new Color(cl(n >> 16 & 255), cl(n >> 8 & 255), cl(n & 255), a);
      };

      shadeHex = (hex, f) => {
        var n = parseInt(hex.slice(1), 16);

        var cl = v => Math.max(0, Math.min(255, Math.round(v * f)));

        var h = v => ('0' + cl(v).toString(16)).slice(-2);

        return '#' + h(n >> 16 & 255) + h(n >> 8 & 255) + h(n & 255);
      }; // ------------------------------------------------------------------ themes


      THEMES = [{
        name: 'Sunny Street',
        skyTop: '#3FA9F5',
        skyBot: '#C9EDFF',
        sun: [-390, 215, '#FFF3A0'],
        hill: ['#9BE07A', '#8FD86C'],
        grass: ['#7ED957', '#6CCB48'],
        road: '#4B4B55',
        haze: '#E8F6FF',
        cloud: '#FFFFFF',
        tint: '#FFFFFF'
      }, {
        name: 'Sunset Hills',
        skyTop: '#5B4BA8',
        skyBot: '#FFB48A',
        sun: [-150, 120, '#FFD27A'],
        hill: ['#7FBF6A', '#6FAF5C'],
        grass: ['#86C45A', '#76B44A'],
        road: '#4A4350',
        haze: '#FFD9BF',
        cloud: '#FFC9A8',
        tint: '#FFE3CF'
      }, {
        name: 'Starry Night',
        skyTop: '#0B1445',
        skyBot: '#3A4A9A',
        sun: [-380, 215, '#FFF8D6'],
        moon: true,
        stars: true,
        hill: ['#2C5A4A', '#264E40'],
        grass: ['#2F7D4F', '#286E45'],
        road: '#33333D',
        haze: '#4A5BB0',
        cloud: '#8FA0D8',
        tint: '#9AA6D8'
      }, {
        name: 'Snowy Town',
        skyTop: '#9CC9E8',
        skyBot: '#EAF4FB',
        sun: [-390, 215, '#FFFFFF'],
        snow: true,
        hill: ['#F4FAFF', '#E6F1F8'],
        grass: ['#F2F8FC', '#DDEBF5'],
        road: '#55596A',
        haze: '#FFFFFF',
        cloud: '#FFFFFF',
        tint: '#EAF2FF'
      }, {
        name: 'Rainbow Meadow',
        skyTop: '#4FC3F7',
        skyBot: '#E1F5FE',
        sun: [-400, 225, '#FFF3A0'],
        rainbow: true,
        hill: ['#A5E87A', '#92DC68'],
        grass: ['#8AE05F', '#78D44E'],
        road: '#4B4B55',
        haze: '#F0FBFF',
        cloud: '#FFFFFF',
        tint: '#FFFFFF'
      }]; // ------------------------------------------------------------------ levels

      LEVELS = [{
        name: 'Meet A, B, C',
        mode: 'targets',
        pool: 'ABC',
        goal: 5,
        speed: 6.5,
        theme: 0,
        color: '#FF8A1F'
      }, {
        name: 'Find the Letter',
        mode: 'find',
        pool: 'ABCDEFGH',
        goal: 5,
        speed: 7,
        theme: 1,
        color: '#FF5A7A'
      }, {
        name: 'Alphabet Order',
        mode: 'order',
        pool: 'ABCDEFGH',
        seq: 'ABCDEFGH',
        goal: 8,
        speed: 7,
        theme: 2,
        color: '#6A5CFF'
      }, {
        name: 'Spell Words',
        mode: 'word',
        pool: 'BUSCATMNR',
        words: ['BUS', 'CAT'],
        goal: 6,
        speed: 7,
        theme: 3,
        color: '#2FA8FF'
      }, {
        name: 'Word Master',
        mode: 'word',
        pool: 'DOGSUNTARMBCL',
        words: ['DOG', 'SUN', 'STAR'],
        goal: 10,
        speed: 7.5,
        theme: 4,
        color: '#22C55E'
      }];

      _export("GameMain", GameMain = (_dec = ccclass('GameMain'), _dec(_class = class GameMain extends Component {
        constructor() {
          super(...arguments);
          this.frames = {};
          this.built = false;
          // driving state
          this.busX = 0;
          this.v = 0;
          this.dist = 0;
          this.t = 0;
          this.keyL = false;
          this.keyR = false;
          this.touchL = false;
          this.touchR = false;
          this.steerSmooth = 0;
          this.hornCool = 0;
          this.brakeHeld = false;
          this.shake = 0;
          // level state
          this.levelIdx = 0;
          this.lvl = LEVELS[0];
          this.th = THEMES[0];
          this.playing = false;
          this.finishing = false;
          this.dirty = true;
          this.done = 0;
          this.mistakes = 0;
          this.need = '';
          this.wordIdx = 0;
          this.letterIdx = 0;
          this.lastTarget = '';
          this.instr = 'Collect the letters!';
          this.save = {
            stars: 3,
            best: [0, 0, 0, 0, 0]
          };
          // spawning
          this.genLetter = 16;
          this.genTree = 1;
          this.genHouse = 6;
          this.vanDist = 40;
          this.bubbleTimer = 0;
          this.items = [];
          this.snow = [];
          // nodes
          this.skyG = void 0;
          this.hazeG = void 0;
          this.snowG = void 0;
          this.worldRoot = void 0;
          this.itemsRoot = void 0;
          this.hud = void 0;
          this.ui = void 0;
          this.menuRoot = void 0;
          this.doneRoot = void 0;
          this.groundG = void 0;
          this.wheel = void 0;
          this.mirror = void 0;
          this.starIcon = void 0;
          this.starsLbl = void 0;
          this.progLbl = void 0;
          this.speedLbl = void 0;
          this.bubbleLbl = void 0;
          this.bubble = void 0;
          this.cardNode = void 0;
          this.cardSpr = void 0;
          this.cardUT = void 0;
          this.levelLbl = void 0;
          this.progStars = [];
          this.clouds = [];
          this.hornSpr = void 0;
          this.brakeSpr = void 0;
          this.banner = void 0;
          this.bannerLbl = void 0;
          this.audio = null;
        }

        // ------------------------------------------------------------ life-cycle
        onLoad() {
          view.setDesignResolutionSize(W, H, ResolutionPolicy.SHOW_ALL);
          this.ensureCanvas();
          this.loadSave();
          Promise.all(FILES.map(n => this.loadFrame(n))).then(() => {
            this.build();
            this.built = true;
          });
          input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
          input.on(Input.EventType.KEY_UP, this.onKeyUp, this);
          input.on(Input.EventType.TOUCH_START, () => this.ac(), this);
        }

        onDestroy() {
          input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
          input.off(Input.EventType.KEY_UP, this.onKeyUp, this);
        }

        ensureCanvas() {
          var ut = this.node.getComponent(UITransform);
          if (!ut) ut = this.node.addComponent(UITransform);
          ut.setContentSize(W, H);
          var cv = this.node.getComponent(Canvas);
          if (!cv) cv = this.node.addComponent(Canvas);

          if (!cv.cameraComponent) {
            var cam = this.node.getComponentInChildren(Camera);

            if (!cam) {
              var cn = new Node('Camera');
              cn.layer = Layers.Enum.UI_2D;
              cn.parent = this.node;
              cn.setPosition(0, 0, 1000);
              cam = cn.addComponent(Camera);
              cam.projection = Camera.ProjectionType.ORTHO;
              cam.orthoHeight = H / 2;
              cam.near = 1;
              cam.far = 2000;
              cam.visibility = Layers.Enum.UI_2D;
            }

            cam.clearFlags = Camera.ClearFlag.SOLID_COLOR;
            cam.clearColor = C('#000000');
            cv.cameraComponent = cam;
          }
        }

        loadFrame(name) {
          return new Promise(res => {
            resources.load("textures/" + name + "/spriteFrame", SpriteFrame, (e, sf) => {
              if (!e && sf) {
                this.frames[name] = sf;
                res();
                return;
              }

              resources.load("textures/" + name, ImageAsset, (e2, img) => {
                if (!e2 && img) {
                  var s = new SpriteFrame();
                  var tex = new Texture2D();
                  tex.image = img;
                  s.texture = tex;
                  this.frames[name] = s;
                } else {
                  console.warn('missing texture', name);
                }

                res();
              });
            });
          });
        } // ------------------------------------------------------------ save data


        loadSave() {
          try {
            var raw = sys.localStorage.getItem(SAVE_KEY);

            if (raw) {
              var s = JSON.parse(raw);

              if (s && typeof s.stars === 'number' && Array.isArray(s.best)) {
                this.save = {
                  stars: s.stars,
                  best: LEVELS.map((_, i) => s.best[i] || 0)
                };
              }
            }
          } catch (e) {
            /* ignore */
          }
        }

        writeSave() {
          try {
            sys.localStorage.setItem(SAVE_KEY, JSON.stringify(this.save));
          } catch (e) {
            /* ignore */
          }
        }

        isUnlocked(i) {
          return i === 0 || this.save.best[i - 1] > 0;
        } // ------------------------------------------------------------- node utils


        mk(name, parent, x, y) {
          if (x === void 0) {
            x = 0;
          }

          if (y === void 0) {
            y = 0;
          }

          var n = new Node(name);
          n.layer = Layers.Enum.UI_2D;
          n.parent = parent;
          n.setPosition(x, y, 0);
          return n;
        }

        spr(parent, frame, w, h, x, y, ay) {
          if (ay === void 0) {
            ay = 0.5;
          }

          var n = this.mk(frame, parent, x, y);
          var ut = n.addComponent(UITransform);
          ut.setContentSize(w, h);
          ut.setAnchorPoint(0.5, ay);
          var s = n.addComponent(Sprite);
          s.sizeMode = Sprite.SizeMode.CUSTOM;
          s.spriteFrame = this.frames[frame] || null;
          return n;
        }

        ratio(frame) {
          var sf = this.frames[frame];
          return sf ? sf.rect.width / sf.rect.height : 1;
        }

        lbl(parent, text, size, x, y, color, outline, ow) {
          if (ow === void 0) {
            ow = 4;
          }

          var n = this.mk('label', parent, x, y);
          n.addComponent(UITransform);
          var l = n.addComponent(Label);
          l.useSystemFont = true;
          l.fontFamily = FONT;
          l.string = text;
          l.fontSize = size;
          l.lineHeight = size + 8;
          l.isBold = true;
          l.color = C(color);
          l.horizontalAlign = Label.HorizontalAlign.CENTER;
          l.verticalAlign = Label.VerticalAlign.CENTER;
          l.overflow = Label.Overflow.NONE;

          if (outline) {
            l.enableOutline = true;
            l.outlineColor = C(outline);
            l.outlineWidth = ow;
          }

          return l;
        }

        poly(g, pts, color) {
          g.fillColor = color;
          g.moveTo(pts[0], pts[1]);

          for (var i = 2; i < pts.length; i += 2) g.lineTo(pts[i], pts[i + 1]);

          g.close();
          g.fill();
        }
        /** Rounded, glossy push-button drawn with Graphics. */


        btn(parent, text, color, x, y, w, h, cb, fontSize) {
          if (fontSize === void 0) {
            fontSize = 0;
          }

          var n = this.mk('btn', parent, x, y);
          n.addComponent(UITransform).setContentSize(w, h);
          var g = n.addComponent(Graphics);
          g.fillColor = shade(color, 0.6);
          g.roundRect(-w / 2, -h / 2 - 7, w, h, h / 3);
          g.fill();
          g.fillColor = C(color);
          g.roundRect(-w / 2, -h / 2, w, h, h / 3);
          g.fill();
          g.fillColor = new Color(255, 255, 255, 70);
          g.roundRect(-w / 2 + 8, 2, w - 16, h / 2 - 8, h / 5);
          g.fill();
          g.lineWidth = 4;
          g.strokeColor = C('#FFFFFF');
          g.roundRect(-w / 2, -h / 2, w, h, h / 3);
          g.stroke();
          this.lbl(n, text, fontSize || Math.round(h * 0.46), 0, 0, '#FFFFFF', shadeHex(color, 0.55), 4);
          n.on(Node.EventType.TOUCH_START, () => n.setScale(0.94, 0.94, 1), this);
          n.on(Node.EventType.TOUCH_CANCEL, () => n.setScale(1, 1, 1), this);
          n.on(Node.EventType.TOUCH_END, () => {
            n.setScale(1, 1, 1);
            this.ac();
            cb();
          }, this);
          return n;
        }
        /** Full-screen dimmer that also swallows touches. */


        overlay(parent, name) {
          var n = this.mk(name, parent);
          n.addComponent(UITransform).setContentSize(W, H);
          var g = n.addComponent(Graphics);
          g.fillColor = new Color(10, 20, 50, 150);
          g.rect(-W / 2, -H / 2, W, H);
          g.fill();
          n.on(Node.EventType.TOUCH_START, () => {
            /* swallow */
          }, this);
          n.on(Node.EventType.TOUCH_END, () => {
            /* swallow */
          }, this);
          return n;
        } // ------------------------------------------------------------------ build


        build() {
          var root = this.node; // 1. sky (themed, redrawn per level)

          this.skyG = this.mk('Sky', root).addComponent(Graphics); // 2. clouds

          var cloudRoot = this.mk('Clouds', root);
          [[-420, 215, 0.9], [120, 245, 0.7], [470, 190, 1.0]].forEach(_ref => {
            var [x, y, s] = _ref;
            var c = this.spr(cloudRoot, 'vfx_smoke_puff', 260 * s, 260 * s * 0.67, x, y);
            c.addComponent(UIOpacity).opacity = 235;
            this.clouds.push(c);
          }); // 3. world

          this.worldRoot = this.mk('World', root);
          this.groundG = this.mk('Ground', this.worldRoot).addComponent(Graphics);
          this.hazeG = this.mk('Haze', this.worldRoot).addComponent(Graphics);
          this.itemsRoot = this.mk('Items', this.worldRoot); // 3b. snow (only in snowy theme)

          this.snowG = this.mk('Snow', root).addComponent(Graphics);

          for (var i = 0; i < 70; i++) {
            this.snow.push({
              x: (Math.random() - 0.5) * W,
              y: (Math.random() - 0.5) * H,
              s: 2 + Math.random() * 3,
              v: 40 + Math.random() * 60
            });
          } // 4. cabin


          var cabin = this.mk('Cabin', root).addComponent(Graphics);
          this.drawCabin(cabin); // 5. dashboard props

          var cab = this.mk('CabinProps', root);
          this.spr(cab, 'dashboard', 210, 96, 330, -192);
          this.mirror = this.spr(cab, 'rearview_mirror', 140, 140 / this.ratio('rearview_mirror'), 335, 228);
          this.spr(cab, 'speedometer', 122, 122, -330, -212);
          this.speedLbl = this.lbl(cab, '0 km/h', 22, -330, -284, '#FFFFFF', '#7A4B00', 4);
          this.wheel = this.spr(cab, 'steering_wheel', 292, 292 / this.ratio('steering_wheel'), 0, -168); // 6. HUD

          this.hud = this.mk('HUD', root);
          this.buildHud(); // 7. menu / level-complete layer

          this.ui = this.mk('UI', root); // 8. letterbox bars

          var bars = this.mk('Letterbox', root).addComponent(Graphics);
          bars.fillColor = C('#000000');
          bars.rect(W / 2, -1200, 1600, 2400);
          bars.rect(-W / 2 - 1600, -1200, 1600, 2400);
          bars.rect(-3000, H / 2, 6000, 1200);
          bars.rect(-3000, -H / 2 - 1200, 6000, 1200);
          bars.fill(); // start on level 1 behind the level-select menu

          this.startLevel(0);
          this.playing = false;
          this.showMenu();
        } // ----------------------------------------------------------------- theme


        applyTheme(i) {
          var th = THEMES[i];
          this.th = th;
          this.drawSky(this.skyG, th);
          var h = this.hazeG;
          h.clear();

          for (var k = 0; k < 8; k++) {
            h.fillColor = C(th.haze, Math.round(120 * (1 - k / 8)));
            h.rect(-1400, HOR - 6 - k * 4, 2800, 5);
            h.fill();
          }

          this.clouds.forEach(c => c.getComponent(Sprite).color = C(th.cloud));
          if (!th.snow) this.snowG.clear();
        }

        drawSky(g, th) {
          g.clear();
          var top = C(th.skyTop);
          var bot = C(th.skyBot);
          var bands = 22;
          var y0 = HOR;
          var hh = H / 2 - y0 + 40;

          for (var i = 0; i < bands; i++) {
            var c = new Color();
            Color.lerp(c, bot, top, i / (bands - 1));
            g.fillColor = c;
            g.rect(-W, y0 + hh / bands * i, W * 2, hh / bands + 1);
            g.fill();
          }

          if (th.stars) {
            var seed = 12345;

            var rnd = () => {
              seed = seed * 1103515245 + 12345 & 0x7fffffff;
              return seed / 0x7fffffff;
            };

            for (var _i = 0; _i < 90; _i++) {
              var _sx = (rnd() - 0.5) * W;

              var _sy = HOR + 40 + rnd() * (H / 2 - HOR - 40);

              g.fillColor = new Color(255, 255, 255, 120 + Math.floor(rnd() * 135));
              g.circle(_sx, _sy, 1 + rnd() * 2.2);
              g.fill();
            }
          }

          if (th.rainbow) {
            var cols = ['#FF4D4D', '#FF9A1A', '#FFE14D', '#4CD964', '#3AA8FF', '#7A5CFF'];
            g.lineWidth = 15;
            cols.forEach((cc, k) => {
              var r = 245 - k * 15;
              g.strokeColor = C(cc, 215);

              for (var s = 0; s <= 48; s++) {
                var a = Math.PI * s / 48;
                var px = 230 + r * Math.cos(a);
                var py = HOR - 10 + r * Math.sin(a);
                if (s === 0) g.moveTo(px, py);else g.lineTo(px, py);
              }

              g.stroke();
            });
          } // sun / moon with glow


          var [sx, sy, sc] = th.sun;
          [[96, 40], [72, 70], [52, 130], [40, 255]].forEach(_ref2 => {
            var [r, a] = _ref2;
            g.fillColor = C(sc, a);
            g.circle(sx, sy, th.moon ? r * 0.9 : r);
            g.fill();
          });

          if (th.moon) {
            g.fillColor = C('#E4DDB5');
            [[-10, 8, 7], [12, -10, 5], [8, 14, 4]].forEach(_ref3 => {
              var [dx, dy, r] = _ref3;
              g.circle(sx + dx, sy + dy, r);
              g.fill();
            });
          } // distant hills


          var hills = [[-520, 90, 60], [-200, 110, 46], [150, 95, 58], [480, 120, 50], [760, 100, 60], [-800, 100, 55]];
          hills.forEach((h, i) => {
            g.fillColor = C(th.hill[i % 2]);
            g.ellipse(h[0], HOR, h[1] + 60, h[2]);
            g.fill();
          });
        }

        drawCabin(g) {
          var X = 740;
          var yellow = C('#FFC61A');
          g.fillColor = yellow;
          g.moveTo(-X, H / 2 + 10);
          g.lineTo(X, H / 2 + 10);
          g.lineTo(X, 295);
          g.quadraticCurveTo(0, 252, -X, 295);
          g.close();
          g.fill();
          g.fillColor = C('#FFE066');
          g.moveTo(-X, H / 2 + 10);
          g.lineTo(X, H / 2 + 10);
          g.lineTo(X, 350);
          g.lineTo(-X, 350);
          g.close();
          g.fill();
          g.lineWidth = 8;
          g.strokeColor = C('#B87400');
          g.moveTo(-X, 295);
          g.quadraticCurveTo(0, 252, X, 295);
          g.stroke();
          this.poly(g, [-X, H / 2 + 10, -520, H / 2 + 10, -588, -170, -X, -170], yellow);
          this.poly(g, [X, H / 2 + 10, 520, H / 2 + 10, 588, -170, X, -170], yellow);
          g.lineWidth = 8;
          g.strokeColor = C('#B87400');
          g.moveTo(-520, 300);
          g.lineTo(-588, -170);
          g.stroke();
          g.moveTo(520, 300);
          g.lineTo(588, -170);
          g.stroke();
          this.poly(g, [-470, 270, -380, 270, -500, -60, -560, -60], C('#FFFFFF', 28));
          g.fillColor = C('#F4A300');
          g.moveTo(-X, -420);
          g.lineTo(-X, -205);
          g.quadraticCurveTo(0, -95, X, -205);
          g.lineTo(X, -420);
          g.close();
          g.fill();
          g.fillColor = C('#FFC93C');
          g.moveTo(-X, -205);
          g.quadraticCurveTo(0, -95, X, -205);
          g.lineTo(X, -240);
          g.quadraticCurveTo(0, -132, -X, -240);
          g.close();
          g.fill();
          g.fillColor = C('#E08F00');
          g.rect(-X, -420, X * 2, 95);
          g.fill();
          g.lineWidth = 9;
          g.strokeColor = C('#2E2A25');
          g.moveTo(-X, -203);
          g.quadraticCurveTo(0, -93, X, -203);
          g.stroke();
        }

        buildHud() {
          var hud = this.hud;
          this.lbl(hud, 'ABC Fun School Bus', 56, 0, 322, '#FFFFFF', '#D9480F', 7);
          this.starIcon = this.spr(hud, 'star_golden', 58, 56, -585, 322);
          this.starsLbl = this.lbl(hud, "Stars: " + this.save.stars, 34, -445, 320, '#FFFFFF', '#8A4B00', 5); // level badge + menu button (top-left, on the windshield glass)

          this.levelLbl = this.lbl(hud, 'Level 1', 26, -520, 262, '#FFFFFF', '#1F6FB5', 5);
          this.btn(hud, 'Menu', '#2F9BFF', -520, 218, 120, 44, () => this.showMenu(), 24); // progress bar

          var bw = 300;
          var bh = bw / this.ratio('progressbar_frame');
          var bar = this.mk('ProgressBar', hud, 480, 322);
          this.spr(bar, 'progressbar_frame', bw, bh, 0, 0);
          var cx = [0.119, 0.311, 0.5, 0.69, 0.879];

          for (var i = 0; i < 5; i++) {
            var s = this.spr(bar, 'star_golden', bh * 0.62, bh * 0.6, (cx[i] - 0.5) * bw, 0);
            this.progStars.push(s);
          }

          this.progLbl = this.lbl(hud, '', 22, 480, 274, '#FFFFFF', '#1F6FB5', 4); // instruction bubble

          this.bubble = this.mk('Bubble', hud, 0, 226);
          this.spr(this.bubble, 'speech_bubble', 300, 112, 0, 0);
          this.bubbleLbl = this.lbl(this.bubble, this.instr, 27, 0, 8, '#D9480F');
          tween(this.bubble).repeatForever(tween().to(0.8, {
            scale: new Vec3(1.04, 1.04, 1)
          }, {
            easing: 'sineInOut'
          }).to(0.8, {
            scale: new Vec3(1, 1, 1)
          }, {
            easing: 'sineInOut'
          })).start(); // target-letter card (find / order / spell levels)

          this.cardNode = this.mk('TargetCard', hud, -222, 226);
          var cg = this.cardNode.addComponent(Graphics);
          cg.fillColor = C('#FFFFFF');
          cg.circle(0, 0, 50);
          cg.fill();
          cg.lineWidth = 7;
          cg.strokeColor = C('#FF8A1F');
          cg.circle(0, 0, 50);
          cg.stroke();
          var cs = this.spr(this.cardNode, 'letter_A', 64, 64, 0, 0);
          this.cardSpr = cs.getComponent(Sprite);
          this.cardUT = cs.getComponent(UITransform);
          this.cardNode.active = false; // steering arrows

          var left = this.spr(hud, 'button_arrow_left', 200, 200, -525, -245);
          var right = this.spr(hud, 'button_arrow_right', 200, 200, 525, -245);
          this.bindBtn(left, () => {
            this.touchL = true;
            left.setScale(0.9, 0.9, 1);
          }, () => {
            this.touchL = false;
            left.setScale(1, 1, 1);
          });
          this.bindBtn(right, () => {
            this.touchR = true;
            right.setScale(0.9, 0.9, 1);
          }, () => {
            this.touchR = false;
            right.setScale(1, 1, 1);
          }); // horn + brake

          var horn = this.spr(hud, 'button_horn', 108, 108, -190, -292);
          var brake = this.spr(hud, 'button_brake', 108, 108, 190, -292);
          this.hornSpr = horn.getComponent(Sprite);
          this.brakeSpr = brake.getComponent(Sprite);
          this.lbl(hud, 'HORN', 22, -190, -228, '#FFFFFF', '#1E7B1E', 4);
          this.lbl(hud, 'BRAKE', 22, 190, -228, '#FFFFFF', '#A51D1D', 4);
          this.bindBtn(horn, () => this.pressHorn(true), () => this.pressHorn(false));
          this.bindBtn(brake, () => this.pressBrake(true), () => this.pressBrake(false)); // banner for level start / spelled words

          this.banner = this.mk('Banner', hud, 0, 100);
          this.bannerLbl = this.lbl(this.banner, '', 64, 0, 0, '#FFE066', '#D9480F', 8);
          this.banner.active = false;
        }

        bindBtn(n, down, up) {
          n.on(Node.EventType.TOUCH_START, down, this);
          n.on(Node.EventType.TOUCH_END, up, this);
          n.on(Node.EventType.TOUCH_CANCEL, up, this);
        } // ------------------------------------------------------------------ menus


        clearUI() {
          if (this.menuRoot && this.menuRoot.isValid) this.menuRoot.destroy();
          if (this.doneRoot && this.doneRoot.isValid) this.doneRoot.destroy();
        }

        showMenu() {
          this.clearUI();
          this.playing = false;
          var m = this.mk('Menu', this.ui);
          this.menuRoot = m;
          this.overlay(m, 'dim');
          this.lbl(m, 'Choose a Level', 58, 0, 225, '#FFFFFF', '#D9480F', 8);
          this.lbl(m, 'Drive into the right letters to win stars!', 26, 0, 170, '#FFFFFF', '#1F3F7A', 5);
          var cw = 200,
              gap = 18;
          var x0 = -((LEVELS.length - 1) * (cw + gap)) / 2;
          LEVELS.forEach((lv, i) => {
            var unlocked = this.isUnlocked(i);
            var card = this.mk('card' + i, m, x0 + i * (cw + gap), -20);
            card.addComponent(UITransform).setContentSize(cw, 290);
            var g = card.addComponent(Graphics);
            g.fillColor = shade(lv.color, 0.6);
            g.roundRect(-cw / 2, -145 - 8, cw, 290, 28);
            g.fill();
            g.fillColor = C(lv.color);
            g.roundRect(-cw / 2, -145, cw, 290, 28);
            g.fill();
            g.fillColor = new Color(255, 255, 255, 60);
            g.roundRect(-cw / 2 + 10, 20, cw - 20, 115, 20);
            g.fill();
            g.lineWidth = 5;
            g.strokeColor = C('#FFFFFF');
            g.roundRect(-cw / 2, -145, cw, 290, 28);
            g.stroke();
            this.lbl(card, String(i + 1), 84, 0, 80, '#FFFFFF', shadeHex(lv.color, 0.5), 6);
            this.lbl(card, lv.name, 23, 0, -5, '#FFFFFF', shadeHex(lv.color, 0.5), 4);
            this.lbl(card, THEMES[lv.theme].name, 16, 0, -38, '#FFFFFF', shadeHex(lv.color, 0.5), 3); // earned stars

            for (var s = 0; s < 3; s++) {
              var st = this.spr(card, 'star_golden', 44, 43, (s - 1) * 52, -90);
              if (s >= this.save.best[i]) st.getComponent(Sprite).color = new Color(120, 120, 140, 170);
            }

            if (unlocked) {
              card.on(Node.EventType.TOUCH_END, () => {
                this.ac();
                this.startLevel(i);
              }, this);
            } else {
              var lg = this.mk('lock', card).addComponent(Graphics);
              lg.fillColor = new Color(20, 25, 50, 170);
              lg.roundRect(-cw / 2, -145, cw, 290, 28);
              lg.fill();
              lg.lineWidth = 9;
              lg.strokeColor = C('#E5E7EB');
              lg.roundRect(-16, 8, 32, 34, 14);
              lg.stroke();
              lg.fillColor = C('#F5C518');
              lg.roundRect(-30, -28, 60, 46, 10);
              lg.fill();
              lg.fillColor = C('#8A6D00');
              lg.circle(0, -6, 7);
              lg.fill();
            }
          });
          this.lbl(m, 'Arrow keys / A-D steer  -  Space honks  -  S brakes', 20, 0, -230, '#FFFFFF', '#1F3F7A', 4);
        }

        showComplete(earned) {
          this.clearUI();
          this.playing = false;
          var m = this.mk('Done', this.ui);
          this.doneRoot = m;
          this.overlay(m, 'dim');
          var g = this.mk('panel', m).addComponent(Graphics);
          g.fillColor = shade('#FF8A1F', 0.6);
          g.roundRect(-320, -185, 640, 380, 40);
          g.fill();
          g.fillColor = C('#FFF8E7');
          g.roundRect(-320, -178, 640, 380, 40);
          g.fill();
          g.lineWidth = 8;
          g.strokeColor = C('#FF8A1F');
          g.roundRect(-320, -178, 640, 380, 40);
          g.stroke();
          var last = this.levelIdx === LEVELS.length - 1;
          this.lbl(m, last ? 'You did it!' : 'Level Complete!', 58, 0, 135, '#D9480F', '#FFFFFF', 7);
          this.lbl(m, "Level " + (this.levelIdx + 1) + ": " + this.lvl.name, 26, 0, 80, '#7A4B00');

          for (var s = 0; s < 3; s++) {
            var st = this.spr(m, 'star_golden', 100, 98, (s - 1) * 125, -2 + (s === 1 ? 14 : 0));
            if (s >= earned) st.getComponent(Sprite).color = new Color(110, 110, 110, 170);else {
              st.setScale(0, 0, 1);
              tween(st).delay(0.25 + s * 0.3).to(0.35, {
                scale: new Vec3(1, 1, 1)
              }, {
                easing: 'backOut'
              }).start();
            }
          }

          var msg = earned === 3 ? 'Perfect! No mistakes!' : earned === 2 ? 'Great driving!' : 'Good try! Play again for 3 stars!';
          this.lbl(m, msg, 26, 0, -80, '#7A4B00');
          this.btn(m, 'Menu', '#2F9BFF', -215, -135, 180, 66, () => this.showMenu());
          this.btn(m, 'Replay', '#FF9A1A', 0, -135, 180, 66, () => this.startLevel(this.levelIdx));
          if (!last) this.btn(m, 'Next', '#3DDC55', 215, -135, 180, 66, () => this.startLevel(this.levelIdx + 1));else this.btn(m, 'Again', '#3DDC55', 215, -135, 180, 66, () => this.startLevel(0));
          var pup = this.spr(m, 'mascot_puppy', 230, 230 / this.ratio('mascot_puppy'), -470, -30);
          pup.setScale(0, 0, 1);
          tween(pup).to(0.45, {
            scale: new Vec3(1, 1, 1)
          }, {
            easing: 'backOut'
          }).start();
        } // --------------------------------------------------------- level control


        startLevel(i) {
          this.clearUI();
          this.levelIdx = i;
          this.lvl = LEVELS[i];
          this.applyTheme(this.lvl.theme);
          this.items.forEach(it => it.node.destroy());
          this.items = [];
          this.busX = 0;
          this.v = 0;
          this.dist = 0;
          this.steerSmooth = 0;
          this.done = 0;
          this.mistakes = 0;
          this.wordIdx = 0;
          this.letterIdx = 0;
          this.lastTarget = '';
          this.finishing = false;
          this.shake = 0;
          this.bubbleTimer = 0;
          this.setNeed();
          this.updateInstruction();
          this.updateHud();
          this.levelLbl.string = "Level " + (i + 1); // scenery + opening letters

          this.genTree = 1;
          this.genHouse = 6;
          this.vanDist = 60 + Math.random() * 40;

          while (this.genTree < SPAWN_Z) {
            this.addTree(this.genTree);
            this.genTree += 5 + Math.random() * 3;
          }

          while (this.genHouse < SPAWN_Z) {
            this.addHouse(this.genHouse);
            this.genHouse += 12 + Math.random() * 6;
          }

          var opening = [[3.6, -1.2], [9.5, 0.9], [16, -1.4]];
          opening.forEach((_ref4, k) => {
            var [z, x] = _ref4;
            var ch = i === 0 ? 'ABC'[k] : k === 0 && this.need ? this.need : this.pickLetter();
            this.addLetter(ch, z, x);
          });
          this.genLetter = 16;

          while (this.genLetter < SPAWN_Z) {
            this.genLetter += 9;
            this.addLetter(this.pickLetter(), this.genLetter, this.randLane());
          }

          this.playing = true;
          this.dirty = true;
          this.showBanner("Level " + (i + 1), 76, 1.6);
          this.scheduleOnce(() => this.speak(this.spokenInstruction()), 0.8);
        }

        poolArr() {
          return this.lvl.pool.split('');
        }

        setNeed() {
          var L = this.lvl;
          if (L.mode === 'targets') this.need = '';else if (L.mode === 'find') {
            var p = this.poolArr().filter(c => c !== this.lastTarget);
            this.need = p[Math.floor(Math.random() * p.length)];
            this.lastTarget = this.need;
          } else if (L.mode === 'order') this.need = L.seq[Math.min(this.done, L.seq.length - 1)];else this.need = L.words[this.wordIdx][this.letterIdx];
          this.updateCard();
        }

        updateCard() {
          if (!this.need) {
            this.cardNode.active = false;
            return;
          }

          var f = this.frames['letter_' + this.need];
          this.cardSpr.spriteFrame = f || null;
          var r = this.ratio('letter_' + this.need);
          this.cardUT.setContentSize(66 * Math.min(1, r), 66 / Math.max(1, r));
          this.cardNode.active = true;
          this.cardNode.setScale(0.5, 0.5, 1);
          tween(this.cardNode).to(0.25, {
            scale: new Vec3(1, 1, 1)
          }, {
            easing: 'backOut'
          }).start();
        }

        updateInstruction() {
          var L = this.lvl;
          if (L.mode === 'targets') this.instr = 'Collect the letters!';else if (L.mode === 'find') this.instr = "Find the letter " + this.need + "!";else if (L.mode === 'order') this.instr = "Next letter: " + this.need;else {
            var w = L.words[this.wordIdx];
            var shown = w.split('').map((c, k) => k < this.letterIdx ? c : '_').join(' ');
            this.instr = w + ":  " + shown;
          }
          if (this.bubbleTimer <= 0) this.bubbleLbl.string = this.instr;
        }

        spokenInstruction() {
          var L = this.lvl;
          if (L.mode === 'targets') return 'Collect the letters!';
          if (L.mode === 'find') return "Find the letter " + this.need;
          if (L.mode === 'order') return "Collect the letters in order. Start with " + this.need;
          return "Spell " + L.words[this.wordIdx] + ". Start with " + this.need;
        } // ---------------------------------------------------------------- input


        onKeyDown(e) {
          switch (e.keyCode) {
            case KeyCode.ARROW_LEFT:
            case KeyCode.KEY_A:
              this.keyL = true;
              break;

            case KeyCode.ARROW_RIGHT:
            case KeyCode.KEY_D:
              this.keyR = true;
              break;

            case KeyCode.SPACE:
            case KeyCode.KEY_H:
              this.pressHorn(true);
              break;

            case KeyCode.ARROW_DOWN:
            case KeyCode.KEY_S:
              this.pressBrake(true);
              break;
          }
        }

        onKeyUp(e) {
          switch (e.keyCode) {
            case KeyCode.ARROW_LEFT:
            case KeyCode.KEY_A:
              this.keyL = false;
              break;

            case KeyCode.ARROW_RIGHT:
            case KeyCode.KEY_D:
              this.keyR = false;
              break;

            case KeyCode.SPACE:
            case KeyCode.KEY_H:
              this.pressHorn(false);
              break;

            case KeyCode.ARROW_DOWN:
            case KeyCode.KEY_S:
              this.pressBrake(false);
              break;
          }
        }

        pressHorn(down) {
          if (!this.built) return;
          this.hornSpr.spriteFrame = this.frames[down ? 'button_horn_pressed' : 'button_horn'] || this.hornSpr.spriteFrame;

          if (down && this.hornCool <= 0) {
            this.hornCool = 0.5;
            this.tone(392, 0.55, 'square', 0.12);
            this.tone(311, 0.55, 'square', 0.12);
            if (this.playing && !this.finishing) this.say('Beep beep!', 1.0);
          }
        }

        pressBrake(down) {
          if (!this.built) return;
          this.brakeHeld = down;
          this.brakeSpr.spriteFrame = this.frames[down ? 'button_brake_pressed' : 'button_brake'] || this.brakeSpr.spriteFrame;
        } // ---------------------------------------------------------------- audio


        ac() {
          try {
            if (!this.audio) {
              var AC = window.AudioContext || window.webkitAudioContext;
              if (AC) this.audio = new AC();
            }

            if (this.audio && this.audio.state === 'suspended') this.audio.resume();
          } catch (e) {
            /* no audio available */
          }

          return this.audio;
        }

        tone(freq, dur, type, vol, delay) {
          if (delay === void 0) {
            delay = 0;
          }

          var a = this.ac();
          if (!a) return;

          try {
            var o = a.createOscillator();
            var g = a.createGain();
            o.type = type;
            var t0 = a.currentTime + delay;
            o.frequency.setValueAtTime(freq, t0);
            g.gain.setValueAtTime(0.0001, t0);
            g.gain.exponentialRampToValueAtTime(vol, t0 + 0.02);
            g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
            o.connect(g);
            g.connect(a.destination);
            o.start(t0);
            o.stop(t0 + dur + 0.05);
          } catch (e) {
            /* ignore */
          }
        }

        speak(text) {
          try {
            var ss = window.speechSynthesis;
            var Utt = window.SpeechSynthesisUtterance;

            if (ss && Utt) {
              ss.cancel();
              var u = new Utt(text);
              u.rate = 0.85;
              u.pitch = 1.3;
              ss.speak(u);
            }
          } catch (e) {
            /* ignore */
          }
        }

        say(text, seconds) {
          this.bubbleLbl.string = text;
          this.bubbleTimer = seconds;
        }

        showBanner(text, size, seconds) {
          this.unschedule(this.hideBanner);
          this.bannerLbl.string = text;
          this.bannerLbl.fontSize = size;
          this.bannerLbl.lineHeight = size + 8;
          this.banner.active = true;
          this.banner.setScale(0, 0, 1);
          tween(this.banner).to(0.35, {
            scale: new Vec3(1, 1, 1)
          }, {
            easing: 'backOut'
          }).start();
          this.scheduleOnce(this.hideBanner, seconds);
        }

        hideBanner() {
          this.banner.active = false;
        } // -------------------------------------------------------------- spawning


        randLane() {
          var lanes = [-1.6, -0.8, 0, 0.8, 1.6];
          return lanes[Math.floor(Math.random() * lanes.length)];
        }

        hasNeededAhead() {
          return this.items.some(it => it.kind === 'letter' && it.ch === this.need && it.z > COLLECT_Z + 0.4);
        }

        pickLetter() {
          var pool = this.poolArr();
          if (this.lvl.mode === 'targets') return pool[Math.floor(Math.random() * pool.length)];
          if (this.need && !this.hasNeededAhead()) return this.need;
          if (this.need && Math.random() < 0.35) return this.need;
          var others = pool.filter(c => c !== this.need);
          return others[Math.floor(Math.random() * others.length)];
        }

        addItem(kind, frame, wm, z, x, vz) {
          if (vz === void 0) {
            vz = 0;
          }

          var node = this.mk(kind, this.itemsRoot);
          var op = node.addComponent(UIOpacity);
          var hm = wm / this.ratio(frame);
          var s = this.spr(node, frame, wm * 100, hm * 100, 0, 0, 0);
          s.getComponent(Sprite).color = C(this.th.tint);
          var it = {
            node,
            op,
            kind,
            z,
            x,
            vz,
            flip: Math.random() < 0.5 ? -1 : 1,
            phase: Math.random() * 6.28
          };
          this.items.push(it);
          return it;
        }

        addTree(z) {
          var side = Math.random() < 0.5 ? -1 : 1;
          this.addItem('tree', 'scenery_trees', 4.2 + Math.random() * 1.4, z, side * (ROAD_HALF + 1.8 + Math.random() * 3.5));
        }

        addHouse(z) {
          var side = Math.random() < 0.5 ? -1 : 1;
          var it = this.addItem('house', 'scenery_houses', 6 + Math.random() * 1.5, z, side * (ROAD_HALF + 5.5 + Math.random() * 3));
          it.flip = 1;
        }

        addVan(z) {
          var it = this.addItem('van', 'traffic_ice_cream_van', 1.9, z, -2.7, 5);
          it.flip = 1;
        }

        addLetter(ch, z, x) {
          var frame = 'letter_' + ch;
          var node = this.mk('letter_' + ch, this.itemsRoot);
          var op = node.addComponent(UIOpacity);
          var sh = this.mk('shadow', node, 0, 2).addComponent(Graphics);
          sh.fillColor = C('#000000', 70);
          sh.ellipse(0, 0, 40, 9);
          sh.fill();
          var bob = this.mk('bob', node, 0, LETTER_CY);
          var r = this.ratio(frame);
          this.spr(bob, frame, 100 * Math.min(r, 1.3), 100 / Math.max(1, r / 1.3), 0, 0);
          var it = {
            node,
            op,
            kind: 'letter',
            z,
            x,
            vz: 0,
            flip: 1,
            phase: Math.random() * 6.28,
            bob,
            ch
          };
          this.items.push(it);
        } // --------------------------------------------------------------- update


        update(dt) {
          if (!this.built) return;
          dt = Math.min(dt, 0.05);
          this.t += dt;
          this.hornCool -= dt; // clouds drift even when paused

          this.clouds.forEach((c, i) => {
            var x = c.position.x + (6 + i * 3) * dt;
            if (x > 900) x = -900;
            c.setPosition(x, c.position.y, 0);
          });
          this.updateSnow(dt);

          if (!this.playing) {
            if (this.dirty) {
              this.drawGround();
              this.items.forEach(it => this.place(it));
              this.sortItems();
              this.dirty = false;
            }

            return;
          } // speed


          if (this.finishing) this.v = Math.max(0, this.v - 5 * dt);else if (this.brakeHeld) this.v = Math.max(0, this.v - BRAKE_DECEL * dt);else this.v = Math.min(this.lvl.speed, this.v + ACCEL * dt);
          var move = this.v * dt;
          this.dist += move; // steering

          var steer = (this.keyR ? 1 : 0) - (this.keyL ? 1 : 0) + (this.touchR ? 1 : 0) - (this.touchL ? 1 : 0);
          steer = Math.max(-1, Math.min(1, steer));
          this.steerSmooth += (steer - this.steerSmooth) * Math.min(1, dt * 8);
          var grip = 0.35 + 0.65 * Math.min(1, this.v / 3);
          this.busX = Math.max(-BUS_LIM, Math.min(BUS_LIM, this.busX + steer * STEER_SPEED * grip * dt));
          this.wheel.angle = -this.steerSmooth * 60; // rumble + shake after a wrong letter

          var rumble = Math.min(1, this.v / this.lvl.speed);
          var sx = 0;

          if (this.shake > 0) {
            this.shake -= dt;
            sx = Math.sin(this.t * 60) * 7 * Math.max(0, this.shake / 0.35);
          }

          this.worldRoot.setPosition(sx, Math.sin(this.t * 17) * 1.3 * rumble, 0);
          this.mirror.angle = Math.sin(this.t * 3.1) * 1.2 * rumble; // generators

          this.genTree -= move;
          this.genHouse -= move;
          this.genLetter -= move;
          this.vanDist -= move;

          while (this.genTree < SPAWN_Z) {
            this.genTree += 5 + Math.random() * 3;
            this.addTree(this.genTree);
          }

          while (this.genHouse < SPAWN_Z) {
            this.genHouse += 12 + Math.random() * 6;
            this.addHouse(this.genHouse);
          }

          if (!this.finishing) {
            while (this.genLetter < SPAWN_Z) {
              this.genLetter += 9;
              this.addLetter(this.pickLetter(), this.genLetter, this.randLane());
            }
          } else if (this.genLetter < SPAWN_Z) this.genLetter = SPAWN_Z;

          if (this.vanDist <= 0) {
            this.vanDist = 70 + Math.random() * 50;
            this.addVan(SPAWN_Z);
          }

          this.drawGround();
          this.updateItems(dt, move);
          this.speedLbl.string = Math.round(this.v * 5) + " km/h";

          if (this.bubbleTimer > 0) {
            this.bubbleTimer -= dt;
            if (this.bubbleTimer <= 0) this.bubbleLbl.string = this.instr;
          }
        }

        updateSnow(dt) {
          if (!this.th.snow) return;
          var g = this.snowG;
          g.clear();
          g.fillColor = new Color(255, 255, 255, 220);

          for (var f of this.snow) {
            f.y -= f.v * dt;
            f.x += Math.sin(this.t * 1.5 + f.s) * 12 * dt;

            if (f.y < -H / 2) {
              f.y = H / 2;
              f.x = (Math.random() - 0.5) * W;
            }

            g.circle(f.x, f.y, f.s);
            g.fill();
          }
        }

        Y(z) {
          return HOR - CAM_H * F / z;
        }

        X(wx, z) {
          return (wx - this.busX) * F / z;
        }

        drawGround() {
          var g = this.groundG;
          g.clear();
          var ZN = 1.0,
              ZF = 1500;
          var R = ROAD_HALF;
          var th = this.th;
          g.fillColor = C(th.grass[0]);
          g.rect(-1400, -800, 2800, HOR + 800);
          g.fill();
          var stripe = 3;

          for (var m = Math.floor(this.dist / stripe); m <= Math.floor((this.dist + 90) / stripe); m++) {
            if (m % 2 === 0) continue;
            var z0 = Math.max(m * stripe - this.dist, ZN);
            var z1 = Math.min((m + 1) * stripe - this.dist, 90);
            if (z1 <= z0) continue;
            this.poly(g, [-1400, this.Y(z0), 1400, this.Y(z0), 1400, this.Y(z1), -1400, this.Y(z1)], C(th.grass[1]));
          }

          this.poly(g, [this.X(-R, ZN), this.Y(ZN), this.X(R, ZN), this.Y(ZN), this.X(R, ZF), this.Y(ZF), this.X(-R, ZF), this.Y(ZF)], C(th.road));
          var ks = 2;

          for (var _m = Math.floor(this.dist / ks); _m <= Math.floor((this.dist + 60) / ks); _m++) {
            var _z = Math.max(_m * ks - this.dist, ZN);

            var _z2 = Math.min((_m + 1) * ks - this.dist, 60);

            if (_z2 <= _z) continue;
            var col = C(_m % 2 === 0 ? '#FF5A5F' : '#FFFFFF');

            for (var s of [-1, 1]) {
              var a = s * R,
                  b = s * (R + 0.45);
              this.poly(g, [this.X(a, _z), this.Y(_z), this.X(b, _z), this.Y(_z), this.X(b, _z2), this.Y(_z2), this.X(a, _z2), this.Y(_z2)], col);
            }
          }

          for (var _s of [-1, 1]) {
            var _a = _s * R,
                _b = _s * (R + 0.45);

            this.poly(g, [this.X(_a, 60), this.Y(60), this.X(_b, 60), this.Y(60), this.X(_b, ZF), this.Y(ZF), this.X(_a, ZF), this.Y(ZF)], C('#F2D7D7'));
          }

          for (var _s2 of [-1, 1]) {
            var _a2 = _s2 * (R - 0.55),
                _b2 = _s2 * (R - 0.4);

            this.poly(g, [this.X(_a2, ZN), this.Y(ZN), this.X(_b2, ZN), this.Y(ZN), this.X(_b2, ZF), this.Y(ZF), this.X(_a2, ZF), this.Y(ZF)], C('#FFFFFF'));
          }

          var per = 5,
              dash = 2.5;

          for (var _m2 = Math.floor(this.dist / per); _m2 <= Math.floor((this.dist + 90) / per); _m2++) {
            var _z3 = Math.max(_m2 * per - this.dist, ZN);

            var _z4 = Math.min(_m2 * per + dash - this.dist, 90);

            if (_z4 <= _z3) continue;
            this.poly(g, [this.X(-0.1, _z3), this.Y(_z3), this.X(0.1, _z3), this.Y(_z3), this.X(0.1, _z4), this.Y(_z4), this.X(-0.1, _z4), this.Y(_z4)], C('#FFD84A'));
          }
        }

        sortItems() {
          this.items.sort((a, b) => b.z - a.z);

          for (var i = 0; i < this.items.length; i++) {
            if (this.items[i].node.getSiblingIndex() !== i) this.items[i].node.setSiblingIndex(i);
          }
        }

        updateItems(dt, move) {
          for (var i = this.items.length - 1; i >= 0; i--) {
            var it = this.items[i];
            it.z -= move + it.vz * dt;

            if (it.kind === 'letter' && !this.finishing && it.z <= COLLECT_Z && Math.abs(it.x - this.busX) < 0.6) {
              this.items.splice(i, 1);
              this.hit(it);
              continue;
            }

            if (it.z <= 0.8) {
              it.node.destroy();
              this.items.splice(i, 1);
              continue;
            }

            this.place(it);
          }

          this.sortItems();
        }

        place(it) {
          var z = it.z;
          var s = F / z / 100;
          it.node.setPosition(this.X(it.x, z), this.Y(z), 0);
          it.node.setScale(s * it.flip, s, 1);
          var a = 1;
          if (z > 45) a = Math.max(0, (SPAWN_Z - z) / (SPAWN_Z - 45));
          if (z < 1.4) a = Math.max(0, (z - 0.8) / 0.6);
          it.op.opacity = Math.round(a * 255);

          if (it.bob) {
            it.bob.setPosition(0, LETTER_CY + Math.sin(this.t * 3 + it.phase) * 8, 0);
            it.bob.angle = Math.sin(this.t * 2 + it.phase) * 7; // the letter we are looking for gently pulses

            var isTarget = !!this.need && it.ch === this.need;
            var sc = isTarget ? 1 + 0.09 * Math.sin(this.t * 6) : 1;
            it.bob.setScale(sc, sc, 1);
          }
        } // ------------------------------------------------------------ collecting


        hit(it) {
          var ch = it.ch;
          var correct = this.lvl.mode === 'targets' || ch === this.need;
          if (correct) this.correct(it, ch);else this.wrong(it, ch);
        }

        screenPos(it) {
          var s = F / it.z / 100;
          return [this.X(it.x, it.z), this.Y(it.z) + LETTER_CY * s, s];
        }

        correct(it, ch) {
          var [px, py, s] = this.screenPos(it);
          tween(it.node).to(0.35, {
            scale: new Vec3(s * 1.7, s * 1.7, 1)
          }, {
            easing: 'backOut'
          }).call(() => it.node.destroy()).start();
          tween(it.op).to(0.35, {
            opacity: 0
          }).start();
          var burst = this.spr(this.hud, 'vfx_star_burst', 120, 120, px, py);
          burst.setScale(0.4, 0.4, 1);
          tween(burst).to(0.4, {
            scale: new Vec3(2.4, 2.4, 1)
          }, {
            easing: 'quadOut'
          }).call(() => burst.destroy()).start();
          burst.addComponent(UIOpacity);
          tween(burst.getComponent(UIOpacity)).to(0.4, {
            opacity: 0
          }).start();
          var star = this.spr(this.hud, 'star_golden', 64, 62, px, py);
          tween(star).to(0.8, {
            position: this.starIcon.position.clone(),
            scale: new Vec3(0.5, 0.5, 1)
          }, {
            easing: 'cubicIn'
          }).call(() => {
            star.destroy();
            this.onStar();
          }).start();
          this.tone(880, 0.25, 'sine', 0.25);
          this.tone(1320, 0.35, 'sine', 0.25, 0.1); // advance the lesson

          this.done++;
          var L = this.lvl;
          var praise = "Great! " + ch + "!";
          if (L.mode === 'find') this.setNeed();else if (L.mode === 'order') {
            if (this.done < L.goal) this.setNeed();
          } else if (L.mode === 'word') {
            this.letterIdx++;
            var w = L.words[this.wordIdx];

            if (this.letterIdx >= w.length) {
              praise = w + "!";
              this.showBanner(w + "!", 90, 1.5);
              this.tone(523, 0.2, 'triangle', 0.25, 0.15);
              this.tone(659, 0.2, 'triangle', 0.25, 0.3);
              this.tone(784, 0.3, 'triangle', 0.25, 0.45);
              this.wordIdx++;
              this.letterIdx = 0;
            }

            if (this.done < L.goal) this.setNeed();
          }

          if (this.done >= L.goal) {
            this.finishLevel();
            this.say(praise, 6);
            this.speak(praise.replace('!', ''));
            return;
          }

          this.updateInstruction();
          this.say(praise, 1.6);
          this.speak(praise.replace('!', ''));

          if (this.need && !this.hasNeededAhead()) {
            this.addLetter(this.need, 24 + Math.random() * 6, this.randLane());
          }
        }

        wrong(it, ch) {
          var [,, s] = this.screenPos(it);
          this.mistakes++;
          this.shake = 0.35;
          tween(it.node).to(0.3, {
            scale: new Vec3(s * 0.4, s * 0.4, 1)
          }, {
            easing: 'quadIn'
          }).call(() => it.node.destroy()).start();
          tween(it.op).to(0.3, {
            opacity: 0
          }).start();
          this.tone(220, 0.25, 'sawtooth', 0.14);
          this.tone(165, 0.3, 'sawtooth', 0.14, 0.12);
          var hint = this.lvl.mode === 'word' || this.lvl.mode === 'order' || this.lvl.mode === 'find' ? "Oops, that is " + ch + ". Look for " + this.need + "!" : '';
          this.say("Oops! Try " + this.need, 2.2);
          this.speak(hint); // make sure the right letter is on its way

          if (!this.hasNeededAhead()) this.addLetter(this.need, 22 + Math.random() * 6, this.randLane());
        }

        onStar() {
          this.save.stars++;
          this.writeSave();
          this.updateHud();
          tween(this.starIcon).to(0.12, {
            scale: new Vec3(1.35, 1.35, 1)
          }).to(0.18, {
            scale: new Vec3(1, 1, 1)
          }).start();
        }

        finishLevel() {
          this.finishing = true;
          var earned = this.mistakes === 0 ? 3 : this.mistakes <= 2 ? 2 : 1;
          if (earned > this.save.best[this.levelIdx]) this.save.best[this.levelIdx] = earned;
          this.writeSave();
          [523, 659, 784, 1047].forEach((f, k) => this.tone(f, 0.28, 'triangle', 0.25, 0.6 + k * 0.16));
          this.scheduleOnce(() => {
            this.speak('Level complete! Great job!');
            this.showComplete(earned);
          }, 2.0);
        }

        updateHud() {
          this.starsLbl.string = "Stars: " + this.save.stars;
          var shown = Math.min(5, Math.floor(this.done * 5 / this.lvl.goal));
          this.progLbl.string = shown + " of 5";
          this.progStars.forEach((s, i) => s.active = i < shown);
        }

      }) || _class));

      _cclegacy._RF.pop();

      _crd = false;
    }
  };
});
//# sourceMappingURL=8e2d7f4affa2eae46e528165bb2f8576f0cc79d7.js.map