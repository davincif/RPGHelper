#Standard Python Imports
#

#Added Python Libraries
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

#Internal Imports
from RPGSystems.DND5.Enums.classes import Classes
from RPGSystems.DND5.Enums.race import Race
from RPGSystems.DND5.Enums.personality import Personality
from RPGSystems.DND5.Enums.attribute import Attribute
from RPGSystems.DND5.Enums.skill import Skill
from RPGSystems.DND5.Enums.coin import Coin

from RPGSystems.DND5.Characters.tables import *


class CharSheet:
	window = None #the windows to be added on screen by the mainWindow

	header = None #header
	scrolled = None #all the screen

	charComboBox = None #the ComboBox with the character name
	playerNameEntry = None #the entry with the player name
	levelEntry = None #character's level Entry
	levelEntry_id = None #levelEntry connect id
	comboPerso = [] #the comboBox of the char's personalites
	expEntry = None #the char's Expirience Points Entry
	expEntry_id = None #expEntry connect id
	backEndEntry = None #char backend Entry
	sugMaleCB = None #suggestion CheckBox for male names
	sugFemaleCB = None #suggestion CheckBox for female names
	sugMaleCB_id = None
	sugFemaleCB_id = None
	comboRace = None #race ComboBox
	comboClass = None #class ComboBox
	nameStore = None #List of names to suggest ListStore

	attDic = {} # {attribute: Entry}
	attModDic = {} #{att modificator: Entry}

	insp_checkBox = None #Inspiration CheckBox
	profBonusEntry = None #Proficiency Bonus Entry

	stCheckBox = [] #save throw Check Box
	saveTrowLabel = [] #save throw Entry

	skillCheckBox = []
	skillLabel = []
	pwPerception = None #passive wisdom (perception) Entry


	profLang = None #other proficiencies & languages TextView

	armorClass = None #armor class Entry
	initiative = None #initiative Entry
	speed = None #speed Entry
	maxHitPoint = None #maxumim hit points Entry
	curHitPoint = None #current hit points Entry
	tempHitPoints = None #temporary hit points Entry

	DSSCheckBox = [] #death saves successs CheckBox
	DSFCheckBox = [] #death saves failures CheckBox

	atknspells = {} #Name, ATK Bonus and Damage/Type Entry

	coins = {} #coins Entry

	perTraitsTV = None #character PERSONALITY TRAITS TextView
	idealTV = None #character IDEAL TextView
	boundTV = None #character BOUND TextView
	flawsTV = None #character FLAWS TextView

	feturesTraits = None #Feature Traits TextView
	
	def __init__(self, window):
		self.window = window

		self.header = Gtk.HeaderBar(title="RPGHelper")
		self.header.set_subtitle("D&D5 character sheet")
		self.header.props.show_close_button = True
		window.set_titlebar(self.header)
		window.set_resizable(True)
		self.window.set_default_size(100, 700)

		#scrolled panel
		self.scrolled = Gtk.ScrolledWindow()
		self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

		#general box
		ggrid = Gtk.Grid()
		ggrid.set_row_spacing(20)
		ggrid.set_column_spacing(20)
		self.scrolled.add_with_viewport(ggrid)

		######HEAD######
		#head
		headGrid = Gtk.Grid(orientation=Gtk.Orientation.HORIZONTAL)
		headGrid.set_row_spacing(10)
		headGrid.set_column_spacing(10)

		#char name box
		self.nameStore = Gtk.ListStore(str)
		charNameBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.charComboBox = Gtk.ComboBox.new_with_model_and_entry(self.nameStore)
		self.charComboBox.set_entry_text_column(0)
		self.charComboBox.connect("changed", self.on_name_combo_changed)
		charNameBox.pack_start(self.charComboBox, expand=True, fill=True, padding=0)
		charNameBox.pack_start(Gtk.Label("Character Name"), expand=True, fill=False, padding=0)

		#class
		raceBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.comboRace = Gtk.ComboBoxText()
		for i in Classes:
			if i != Classes.NO_CLASS:
				self.comboRace.append_text(i.get_fancy_name())
		raceBox.pack_start(self.comboRace, expand=True, fill=True, padding=0)
		raceBox.pack_start(Gtk.Label("Class"), expand=True, fill=False, padding=0)

		#race
		classBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.comboClass = Gtk.ComboBoxText()
		for i in Race:
			if i != Race.NO_RACE and not i.is_uprace():
				self.comboClass.append_text(i.get_fancy_name())
		classBox.pack_start(self.comboClass, expand=True, fill=True, padding=0)
		classBox.pack_start(Gtk.Label("Race"), expand=True, fill=False, padding=0)

		#player name box
		playerNameBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.playerNameEntry = Gtk.Entry()
		self.playerNameEntry.set_text("Player Name")
		self.playerNameEntry.connect("changed", self.on_name_combo_changed)
		playerNameBox.set_valign(Gtk.Align.CENTER)
		playerNameBox.pack_start(self.playerNameEntry, expand=True, fill=True, padding=0)
		playerNameBox.pack_start(Gtk.Label("Player Name"), expand=True, fill=False, padding=0)

		#Alignment
		AligmentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.comboPerso += [Gtk.ComboBoxText()]
		self.comboPerso += [Gtk.ComboBoxText()]
		for i in Personality:
			if i.is_law():
				self.comboPerso[0].append_text(i.get_fancy_name())
			if i.is_morality():
				self.comboPerso[1].append_text(i.get_fancy_name())
		auxBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
		auxBox.pack_start(self.comboPerso[0], expand=True, fill=True, padding=0)
		auxBox.pack_start(self.comboPerso[1], expand=True, fill=True, padding=0)
		AligmentBox.pack_start(auxBox, expand=True, fill=True, padding=0)
		AligmentBox.pack_start(Gtk.Label("Alignments"), expand=True, fill=False, padding=0)

		#level
		levelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.levelEntry = Gtk.Entry()
		self.levelEntry.set_has_frame(False)
		self.levelEntry.set_max_length(2)
		self.levelEntry.set_text("1")
		self.levelEntry.props.xalign = 0.5
		self.levelEntry_id = self.levelEntry.connect("changed", self.on_change_lvlNexp)
		levelBox.pack_start(self.levelEntry, expand=True, fill=True, padding=0)
		levelBox.pack_start(Gtk.Label("Level"), expand=True, fill=False, padding=0)

		backEndBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.backEndEntry = Gtk.Entry()
		self.backEndEntry.props.xalign = 0.5
		backEndBox.pack_start(self.backEndEntry, expand=True, fill=False, padding=0)
		backEndBox.pack_start(Gtk.Label("Background"), expand=True, fill=False, padding=0)

		#Expirience Points
		expBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.expEntry = Gtk.Entry()
		self.expEntry.set_max_length(6)
		self.expEntry.props.xalign = 0.5
		self.expEntry_id = self.expEntry.connect("changed", self.on_change_lvlNexp)
		expBox.pack_start(self.expEntry, expand=True, fill=True, padding=0)
		expBox.pack_start(Gtk.Label("Expirience"), expand=True, fill=False, padding=0)

		#Suggest Name
		sugName = Gtk.Grid()
		sugName.set_row_spacing(5)
		sugName.set_column_spacing(5)
		self.sugMaleCB = Gtk.CheckButton.new_with_label("Male")
		self.sugMaleCB_id = self.sugMaleCB.connect("toggled", self.on_toggled_suggestion)
		self.sugFemaleCB = Gtk.CheckButton.new_with_label("Female")
		self.sugFemaleCB_id = self.sugFemaleCB.connect("toggled", self.on_toggled_suggestion)
		sugName.attach(Gtk.Label("If you want name suggestion, mark bellow"), left=0, top=0, width=2, height=1)
		sugName.attach(self.sugMaleCB, left=0, top=1, width=1, height=1)
		sugName.attach(self.sugFemaleCB, left=1, top=1, width=1, height=1)


		headGrid.attach(charNameBox, left=0, top=0, width=2, height=2)
		headGrid.attach(classBox, left=2, top=0, width=1, height=1)
		headGrid.attach(raceBox, left=2, top=1, width=1, height=1)
		headGrid.attach(levelBox, left=3, top=0, width=1, height=1)
		headGrid.attach(expBox, left=3, top=1, width=1, height=1)
		headGrid.attach(AligmentBox, left=4, top=0, width=1, height=1)
		headGrid.attach(backEndBox, left=4, top=1, width=1, height=1)
		headGrid.attach(playerNameBox, left=5, top=0, width=2, height=2)
		headGrid.attach(sugName, left=7, top=0, width=1, height=2)
		######HEAD######

		######ATTRIBUTES######
		attBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)
		base_spacing = 0
		n = 0
		for at in Attribute:
			if at != Attribute.NO_ATTRIBUTE:
				auxBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=base_spacing)
				self.attDic[at] = Gtk.Entry()
				self.attDic[at].set_alignment(xalign=0.5)
				self.attDic[at].set_max_length(2)
				self.attDic[at].connect("changed", self.on_att_change, at)
				self.attModDic[at] = Gtk.Entry()
				self.attModDic[at].set_alignment(xalign=0.5)
				self.attModDic[at].set_sensitive(False)
				self.attModDic[at].set_max_length(3)
				auxBox.pack_start(Gtk.Label(at.get_fancy_name()), expand=False, fill=False, padding=0)
				auxBox.pack_start(self.attModDic[at], expand=True, fill=True, padding=0)
				auxBox.pack_start(self.attDic[at], expand=True, fill=True, padding=0)
				attBox.pack_start(auxBox, expand=False, fill=False, padding=0)
				n += 1
		######ATTRIBUTES######

		######INSPIRATION | PROFICIENCY BONUS | SAVING TROWS | SKILLS######
		ipskBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
		######INSPIRATION######
		self.insp_checkBox = Gtk.CheckButton.new_with_label("Inspiration")
		######INSPIRATION######

		######PROFICIENCY BONUS######
		profBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=base_spacing)
		self.profBonusEntry = Gtk.Entry()
		self.profBonusEntry.set_has_frame(False)
		self.profBonusEntry.set_max_length(2)
		self.profBonusEntry.set_sensitive(False)
		self.profBonusEntry.props.xalign = 0.5
		profBox.pack_start(self.profBonusEntry, expand=False, fill=False, padding=0)
		profBox.pack_start(Gtk.Label("Proficiency Bonus"), expand=False, fill=False, padding=0)
		######PROFICIENCY BONUS######

		######SAVING TROWS######
		stBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		n = 0
		for at in Attribute:
			if at != Attribute.NO_ATTRIBUTE:
				auxBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
				self.stCheckBox += [Gtk.CheckButton()]
				self.stCheckBox[n].set_sensitive(False)
				self.saveTrowLabel += [Gtk.Label("______")]
				auxBox.pack_start(self.stCheckBox[n], expand=False, fill=False, padding=0)
				auxBox.pack_start(self.saveTrowLabel[n], expand=False, fill=False, padding=0)
				auxBox.pack_start(Gtk.Label(at.get_fancy_name()), expand=False, fill=False, padding=0)
				stBox.pack_start(auxBox, expand=False, fill=False, padding=0)
				n += 1
		stBox.pack_start(Gtk.Label("SAVING TROWS"), expand=False, fill=False, padding=0)
		stBox.set_valign(Gtk.Align.CENTER)
		######SAVING TROWS######

		######SKILLS######
		aux2Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		n = 0
		for at in Skill:
			if at != Skill.NO_SKILL:
				auxBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
				self.skillCheckBox += [Gtk.CheckButton()]
				self.skillCheckBox[n].set_sensitive(False)
				self.skillLabel += [Gtk.Label("______")]
				auxBox.pack_start(self.skillCheckBox[n], expand=False, fill=False, padding=0)
				auxBox.pack_start(self.skillLabel[n], expand=False, fill=False, padding=0)
				auxBox.pack_start(Gtk.Label(at.get_fancy_name()), expand=False, fill=False, padding=0)
				aux2Box.pack_start(auxBox, expand=False, fill=False, padding=0)
				n += 1
		skillscrolled = Gtk.ScrolledWindow()
		skillscrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		skillscrolled.add_with_viewport(aux2Box)
		skillBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		skillBox.pack_start(skillscrolled, expand=True, fill=True, padding=0)
		skillBox.pack_start(Gtk.Label("SKILLS"), expand=False, fill=False, padding=0)
		skillscrolled.props.min_content_height = 200 #horreble solution, but the only one I found...
		######SKILLS######
		######INSPIRATION | PROFICIENCY BONUS | SAVING TROWS | SKILLS######

		######PASSIVE WISDOM (PERCEPTION)######
		pwBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		self.pwPerception = Gtk.Entry()
		pwBox.pack_start(self.pwPerception, expand=False, fill=False, padding=0)
		pwBox.pack_start(Gtk.Label("passive wisdom (perception)"), expand=False, fill=False, padding=0)
		######PASSIVE WISDOM (PERCEPTION)######

		######OTHER PROFICIENCIES & LANGUAGES######
		plBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.profLang = Gtk.TextView()
		plBox.pack_start(self.profLang, expand=True, fill=True, padding=0)
		plBox.pack_start(Gtk.Label("OTHER PROFICIENCIES & LANGUAGES"), expand=True, fill=True, padding=0)
		######OTHER PROFICIENCIES & LANGUAGES######

		######1º GRAY BOX######
		graybox1 = Gtk.Grid()
		graybox1.set_row_spacing(20)
		graybox1.set_column_spacing(20)

		######ARMOR CLASS######
		armorClassBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.armorClass = Gtk.Entry()
		self.armorClass.set_has_frame(False)
		self.armorClass.set_max_length(3)
		self.armorClass.set_sensitive(False)
		self.armorClass.props.xalign = 0.5
		self.armorClass.set_text("0")
		armorClassBox.pack_start(self.armorClass, expand=True, fill=True, padding=0)
		armorClassBox.pack_start(Gtk.Label("armor class"), expand=False, fill=False, padding=0)
		######ARMOR CLASS######

		######INITIATIVE######
		initiativeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.initiative = Gtk.Entry()
		self.initiative.set_has_frame(False)
		self.initiative.set_max_length(3)
		self.initiative.set_sensitive(False)
		self.initiative.props.xalign = 0.5
		self.initiative.set_text("0")
		initiativeBox.pack_start(self.initiative, expand=True, fill=True, padding=0)
		initiativeBox.pack_start(Gtk.Label("initiative"), expand=False, fill=False, padding=0)
		######INITIATIVE######

		######SPEED######
		speedBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.speed = Gtk.Entry()
		self.speed.set_has_frame(False)
		self.speed.set_max_length(3)
		self.speed.set_sensitive(False)
		self.speed.props.xalign = 0.5
		self.speed.set_text("0")
		speedBox.pack_start(self.speed, expand=True, fill=True, padding=0)
		speedBox.pack_start(Gtk.Label("speed"), expand=False, fill=False, padding=0)
		######SPEED######

		######CURRENT HIT POINTS######
		pointBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		# pointBox.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(65535, 65535, 65535))
		maxhitpoitBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		self.maxHitPoint = Gtk.Entry()
		self.maxHitPoint.set_has_frame(False)
		self.maxHitPoint.set_max_length(3)
		self.maxHitPoint.set_sensitive(False)
		self.maxHitPoint.props.xalign = 0.5
		self.maxHitPoint.set_text("0")	
		maxhitpoitBox.pack_start(Gtk.Label("Hit Point Maximum"), expand=False, fill=False, padding=0)
		maxhitpoitBox.pack_start(self.maxHitPoint, expand=True, fill=True, padding=0)
		curHitpoitBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
		self.curHitPoint = Gtk.Entry()
		self.curHitPoint.set_has_frame(False)
		self.curHitPoint.set_max_length(3)
		self.curHitPoint.set_sensitive(False)
		self.curHitPoint.props.xalign = 0.5
		self.curHitPoint.set_text("0")	
		curHitpoitBox.pack_start(self.curHitPoint, expand=True, fill=True, padding=0)
		curHitpoitBox.pack_start(Gtk.Label("Current Hit Points"), expand=False, fill=False, padding=0)
		pointBox.pack_start(maxhitpoitBox, expand=True, fill=True, padding=0)
		pointBox.pack_start(curHitpoitBox, expand=True, fill=True, padding=0)
		######CURRENT HIT POINTS######

		######TEMPORARY HIT POINTS######
		tempHitBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.tempHitPoints = Gtk.Entry()
		self.tempHitPoints.set_has_frame(False)
		self.tempHitPoints.set_max_length(3)
		self.tempHitPoints.set_sensitive(False)
		self.tempHitPoints.props.xalign = 0.5
		self.tempHitPoints.set_text("0")
		tempHitBox.pack_start(self.tempHitPoints, expand=True, fill=True, padding=0)
		tempHitBox.pack_start(Gtk.Label("Temporary Hit Points"), expand=False, fill=False, padding=0)
		######TEMPORARY HIT POINTS######

		######HIT DICE######
		hitDiceBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		totalHitDiceBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		self.totalHitDice = Gtk.Entry()
		self.totalHitDice.set_has_frame(False)
		self.totalHitDice.set_max_length(3)
		self.totalHitDice.set_sensitive(False)
		self.totalHitDice.props.xalign = 0.5
		self.totalHitDice.set_text("0")	
		totalHitDiceBox.pack_start(Gtk.Label("Total Hit Dice"), expand=False, fill=False, padding=0)
		totalHitDiceBox.pack_start(self.totalHitDice, expand=True, fill=True, padding=0)
		curHitDiceBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
		self.curHitDice = Gtk.Entry()
		self.curHitDice.set_has_frame(False)
		self.curHitDice.set_max_length(3)
		self.curHitDice.set_sensitive(False)
		self.curHitDice.props.xalign = 0.5
		self.curHitDice.set_text("0")	
		curHitDiceBox.pack_start(self.curHitDice, expand=True, fill=True, padding=0)
		curHitDiceBox.pack_start(Gtk.Label("Hit Dice"), expand=False, fill=False, padding=0)
		hitDiceBox.pack_start(totalHitDiceBox, expand=True, fill=True, padding=0)
		hitDiceBox.pack_start(curHitDiceBox, expand=True, fill=True, padding=0)
		######HIT DICE######

		######DEATH SAVES######
		deathSaveBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

		self.DSSCheckBox += [Gtk.CheckButton(), Gtk.CheckButton(), Gtk.CheckButton()]
		auxBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		auxBox.pack_start(Gtk.Label("successes"), expand=False, fill=False, padding=0)
		for cb in self.DSSCheckBox:
			auxBox.pack_start(cb, expand=True, fill=True, padding=0)
		deathSaveBox.pack_start(auxBox, expand=True, fill=True, padding=0)
		
		auxBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		self.DSFCheckBox += [Gtk.CheckButton(), Gtk.CheckButton(), Gtk.CheckButton()]
		auxBox.pack_start(Gtk.Label("failures"), expand=False, fill=False, padding=0)
		for cb in self.DSFCheckBox:
			auxBox.pack_start(cb, expand=True, fill=True, padding=0)
		deathSaveBox.pack_start(auxBox, expand=True, fill=True, padding=0)
		deathSaveBox.pack_start(Gtk.Label("Death Saves"), expand=True, fill=True, padding=0)
		######DEATH SAVES######


		graybox1.attach(armorClassBox, left=0, top=0, width=2, height=1)
		graybox1.attach(initiativeBox, left=3, top=0, width=2, height=1)
		graybox1.attach(speedBox, left=5, top=0, width=2, height=1)
		graybox1.attach(pointBox, left=0, top=1, width=6, height=2)
		graybox1.attach(tempHitBox, left=0, top=3, width=6, height=2)
		graybox1.attach(hitDiceBox, left=0, top=5, width=3, height=2)
		graybox1.attach(deathSaveBox, left=3, top=5, width=3, height=2)
		######1º GRAY BOX######

		######ATTACKS & SPELLCASTING######
		#não sei direito como funciona essa parte
		atksplGrid = Gtk.Grid()
		atksplGrid.set_row_spacing(20)
		atksplGrid.set_column_spacing(20)

		self.atknspells = [("Name", Gtk.Entry()),
							("ATK Bonus", Gtk.Entry()),
							("Damage/Type", Gtk.Entry())]
		n = 0
		for att in self.atknspells:
			auxBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
			auxBox.pack_start(Gtk.Label(att[0]), expand=False, fill=False, padding=0)
			auxBox.pack_start(att[1], expand=True, fill=True, padding=0)
			if att[0] != "ATK Bonus":
				atksplGrid.attach(auxBox, left=n, top=0, width=2, height=1)
				n += 2
			else:
				atksplGrid.attach(auxBox, left=n, top=0, width=1, height=1)
				n += 1
			atksplGrid.attach(Gtk.Button("+"), left=0, top=1, width=5, height=1)
			atksplGrid.attach(Gtk.Label("ATTACKS & SPELLCASTING"), left=0, top=2, width=5, height=1)
		######ATTACKS & SPELLCASTING######

		######EQUIPMENT######
		equipBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
		aux2Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)

		coinsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
		for coin in Coin:
			if coin != Coin.NO_COIN:
				self.coins[coin] = Gtk.Entry()

				auxBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
				auxBox.pack_start(Gtk.Label(coin.get_fancy_name()), expand=True, fill=False, padding=0)
				auxBox.pack_start(self.coins[coin], expand=True, fill=True, padding=0)
				coinsBox.pack_start(auxBox, expand=True, fill=True, padding=0)

		toolsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		toolsBox.pack_start(Gtk.Entry(), expand=False, fill=True, padding=0)
		toolsBox.pack_start(Gtk.Button("+"), expand=False, fill=True, padding=0)

		aux2Box.pack_start(coinsBox, expand=True, fill=True, padding=0)
		aux2Box.pack_start(toolsBox, expand=True, fill=True, padding=0)
		equipBox.pack_start(aux2Box, expand=True, fill=True, padding=0)
		equipBox.pack_start(Gtk.Label("EQUIPMENT & BAG"), expand=True, fill=True, padding=0)
		######EQUIPMENT######

		######2º GRAY BOX######
		graybox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

		self.perTraitsTV = Gtk.TextView()
		self.idealTV = Gtk.TextView()
		self.boundTV = Gtk.TextView()
		self.flawsTV = Gtk.TextView()
		graybox2.pack_start(self.perTraitsTV, expand=True, fill=True, padding=0)
		graybox2.pack_start(Gtk.Label("Personality Traits"), expand=True, fill=True, padding=0)
		graybox2.pack_start(self.idealTV, expand=True, fill=True, padding=0)
		graybox2.pack_start(Gtk.Label("Ideal"), expand=True, fill=True, padding=0)
		graybox2.pack_start(self.boundTV, expand=True, fill=True, padding=0)
		graybox2.pack_start(Gtk.Label("Bonds"), expand=True, fill=True, padding=0)
		graybox2.pack_start(self.flawsTV, expand=True, fill=True, padding=0)
		graybox2.pack_start(Gtk.Label("Flwas"), expand=True, fill=True, padding=0)
		######2º GRAY BOX######

		######FEATURES & TRAITS######
		ftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		self.feturesTraits = Gtk.TextView()
		ftBox.pack_start(self.feturesTraits, expand=True, fill=True, padding=0)
		ftBox.pack_start(Gtk.Label("FEATURES & TRAITS"), expand=False, fill=True, padding=0)
		######FEATURES & TRAITS######

		#final packing on general box
		ggrid.attach(headGrid, left=0, top=0, width=9, height=1) #head
		ggrid.attach(attBox, left=0, top=1, width=1, height=6) #attributes
		ggrid.attach(self.insp_checkBox, left=1, top=1, width=2, height=1) #inspiration
		ggrid.attach(profBox, left=1, top=2, width=2, height=1) #proficiency bonus
		ggrid.attach(stBox, left=1, top=3, width=2, height=2) #save throws
		ggrid.attach(skillBox, left=1, top=5, width=2, height=2) #skill
		ggrid.attach(pwBox, left=0, top=7, width=3, height=1) #passive wis. (perception)
		ggrid.attach(plBox, left=0, top=8, width=3, height=2) #profic. & languages
		ggrid.attach(graybox1, left=4, top=1, width=3, height=4)
		ggrid.attach(atksplGrid, left=4, top=5, width=3, height=2) #attack and spellcasting
		ggrid.attach(equipBox, left=4, top=8, width=3, height=3) #equipaments (bag)
		ggrid.attach(graybox2, left=7, top=1, width=3, height=4) #personality, bonds...
		ggrid.attach(ftBox, left=7, top=5, width=3, height=5) #feature traits

		#put all on window and show
		window.set_position(Gtk.WindowPosition.CENTER)
		window.add(self.scrolled)
		window.show_all()

		#updating field for the first time
		self.on_change_lvlNexp(self.levelEntry)


	#FRONT END
	def on_name_combo_changed(self, widget):
		###
		# capitalize the char and player name
		# ex.: "leo da vinci" -> "Leo Da Vinci"
		###

		if self.playerNameEntry == widget:
			name = widget.get_text()
			entry = widget
		elif self.charComboBox == widget:
			tree_iter = widget.get_active_iter()
			entry = widget.get_child()
			if tree_iter != None:
				model = widget.get_model()
				name = model[tree_iter][0]
			else:
				name = entry.get_text()

		if name != "":
			if name[0] == " ":
				name = ""
			else:
				name = name[0].upper() + name[1:]

			n = 0
			while True:
				n = len(name[:n]) + name[n:].find(" ")
				if n < 0 or n+1 >= len(name) or name[n] != " ":
					break

				name = name[:n+1] + name[n+1].upper() + name[n+2:]
				n += 2

		entry.set_text(name)

	#CALL BACK FUNCTIONS (BACK END)
	def on_change_lvlNexp(self, widget):
		###
		# updates all field related to the level and expirience
		###

		level = None
		exp = None
		profBonus = None

		#update level or expirience
		if widget == self.levelEntry:
			self.expEntry.handler_block(self.expEntry_id)
			try:
				level = int(widget.get_text())
				exp, profBonus = exp_for_level(level)
				self.expEntry.set_text(str(exp))
			except ValueError:
				self.levelEntry.set_text("")
				self.expEntry.set_text("")
			self.expEntry.handler_unblock(self.expEntry_id)
		elif widget == self.expEntry:
			self.levelEntry.handler_block(self.levelEntry_id)
			try:
				exp = int(widget.get_text())
				level, profBonus = lvl_for_exp(exp)
				self.levelEntry.set_text(str(level))
			except ValueError:
				self.levelEntry.set_text("")
			self.levelEntry.handler_unblock(self.levelEntry_id)

		#update the proficiency bonus
		if profBonus is not None:
			self.profBonusEntry.set_text("+" + str(profBonus))

	def on_att_change(self, widget, attType):
		###
		# update all fields affected by the attributes
		###

		try:
			att = int(widget.get_text())
			if att > 30:
				att = 30
				widget.set_text("30")

			mod = mod_by_att(att)
			if mod > 0:
				mod = "+" + str(mod)
			else:
				mod = str(mod)
			self.attModDic[attType].set_text(mod)
		except ValueError:
			widget.set_text("")

	def on_toggled_suggestion(self, widget):
		###
		# add the suggestion name to the character based on the race
		###

		if widget == self.sugMaleCB:
			#suggest male names
			self.sugFemaleCB.handler_block(self.sugFemaleCB_id)

			self.sugFemaleCB.set_active(False)

			# self.nameStore.clear()
			# tree_iter = self.comboRace.get_active_iter()
			# model = self.comboRace.get_model()
			# name = model[tree_iter][0]
			# comboRace
			# [self.nameStore.append([elem]) for elem in suggest_name(Race())]
			
			self.sugFemaleCB.handler_unblock(self.sugFemaleCB_id)
		elif widget == self.sugFemaleCB:
			#suggest famale names
			self.sugMaleCB.handler_block(self.sugMaleCB_id)

			self.sugMaleCB.set_active(False)

			self.sugMaleCB.handler_unblock(self.sugMaleCB_id)
