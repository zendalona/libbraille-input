###########################################################################
#    SBW - Sharada-Braille-Writer
#
#    Copyright (C) 2012-2014 Nalin <nalin.x.linux@gmail.com>
#    Copyright (C) 2021-2022 Nalin <nalin.x.linux@gmail.com>
#    
#    This project is funded by State Council of Educational Research and Training (S.C.E.R.T) Kerala 
#    Supervised by Zendalona(2021-2022) and Keltron(2012-2014)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################


import os
import enum

import re

import locale
from locale import gettext as _
locale.bindtextdomain('libbraille-input', '/usr/share/locale')
locale.textdomain('libbraille-input')

#Liblouis
import louis

liblouis_table_dir = "/usr/share/braille-input/liblouis-back-translation-tables/"

built_in_braille_table_dir = "/usr/share/braille-input/built-in-braille-tables"


class Keys(enum.Enum):
    Dot1 = "1"
    Dot2 = "2"
    Dot3 = "3"
    Dot4 = "4"
    Dot5 = "5"
    Dot6 = "6"
    Dot7 = "7"
    Dot8 = "8"
    
    ToggleBrailleMode = "b"

    Abbreviation = "a"
    Capital = "c"
    LetterDeletion = "h"
    Punctuation = ";"
    OneHandSkip = "t"
    
    LangSwitch = "~"
    BegMidSwitch = "Alt"
    
    
    L1 = "F1"
    L2 = "F2"
    L3 = "F3"
    L4 = "F4"
    L5 = "F5"
    L6 = "F6"
    L7 = "F7" 
    L8 = "F8"
    L9 = "F9"
    L10 = "F10"
    L11 = "F11"
    L12 = "F12"
    BuiltInSel = "Ctrl"
    
    Space = "Space"
    NewLine = "NewLine"
    NewLine2 = "NewLine2"
    
    


    
class BrailleInputEngine():
	

	def __init__(self):
		
		self.keycode_map = {}
		
		self.braille_mode = True
		
		self.language_switch_keycode_list = []
		
		self.language_switch_built_in_mode= False
		
		self.auto_capitalize_sentence = False

		self.auto_capitalize_line = False
		
		self.capitalize_line_start = False
		
		self.capitalize_sentence_start = False

		self.simple_mode = False
		
		self.liblouis_mode = False
		
		self.sigle_line_mode = False
		
		self.liblouis_language_table_conversion_dict = {}
		
		self.pressed_key_list = []
		
		self.language_key_list = [ Keys.L1, Keys.L2, Keys.L3, Keys.L4, Keys.L5, Keys.L6, Keys.L7, Keys.L8, 
		Keys.L9, Keys.L10, Keys.L11, Keys.L12]
		
		self.previous_announced_text = ""

		self.conventional_braille_dot_4 = False;
		self.conventional_braille_dot_4_pass = False;
		self.conventional_braille_dot_3 = False;

		self.event_callback = None

		#Three dot braille
		self.three_dot_pos = 1;

		#Braille Iter's
		self.braille_letter_map_pos = 0;
		
		#capital switch
		self.capital_shift = 0;
		self.caps_lock = 0
		
		self.is_liblouis_typing = False

		# Used with liblouis based engine
		self.last_appeared_word_length = 0;
		self.louis_typing_word_combinations = "";
		
		self.built_in_language_list = []
		self.built_in_language_notify_language_conversion_dict = {}
		for line in open("%s/languages.txt" % built_in_braille_table_dir,'r'):
			language, notify_language = line[:-1].split(" ");
			self.built_in_language_notify_language_conversion_dict[language] = notify_language;
			self.built_in_language_list.append(language)
			
		self.liblouis_language_list = []
		for line in open(liblouis_table_dir+"language-table-dict.txt").readlines():
			language, tablename, notify_language = line[:-1].split(" ");
			self.liblouis_language_table_conversion_dict[language] = (liblouis_table_dir+tablename,notify_language);
			self.liblouis_language_list.append(language)
		
	def set_variables_from_object(self, obj):
		self.set_checked_languages_built_in(obj.checked_languages_built_in)
		self.set_checked_languages_liblouis(obj.checked_languages_liblouis)
		self.set_keycode_map(obj.keycode_map)
		self.set_braille_mode(obj.braille_mode)
		self.set_liblouis_mode(obj.liblouis_mode)
		self.set_auto_capitalize_sentence(obj.auto_capitalize_sentence)
		self.set_auto_capitalize_line(obj.auto_capitalize_line)
		self.set_simple_mode(obj.simple_mode)
		self.set_line_limit(obj.line_limit)
		self.set_conventional_braille(obj.conventional_braille)
		self.set_one_hand_mode(obj.one_hand_mode)
		self.set_one_hand_conversion_delay(obj.one_hand_conversion_delay)
		self.set_notify_callback(obj.notify_function)
		self.set_notification(obj.notification)
		self.set_notify_language_callback(obj.set_notify_language)
		
		if(obj.liblouis_mode):
			self.set_liblouis_language(obj.last_loaded_liblouis_language)
		else:
			self.set_built_in_language(obj.last_loaded_built_in_language)


	def load_default_language(self):
		if (self.liblouis_mode):
			self.set_liblouis_language(self.checked_languages_liblouis[0])
		else:
			self.load_built_in_table(self.checked_languages_built_in[0])
		
	def get_available_built_in_languages(self):
		return self.built_in_language_list


	def get_available_liblouis_languages(self):
		return self.liblouis_language_list
	
	def set_abbreviations(self, abbreviations):
		self.abbreviations = abbreviations

	def set_line_limit(self,limit):
		self.line_limit = limit;

	def set_auto_new_line(self, value):
		self.auto_new_line = value;

	def set_single_line_mode(self, value):
		self.sigle_line_mode = value
	
	def set_keycode_map(self, keycode_map):
		self.keycode_map = keycode_map;

	def set_auto_capitalize_sentence(self, value):
		self.auto_capitalize_sentence = value;

	def set_auto_capitalize_line(self, value):
		self.auto_capitalize_line = value;

	def set_simple_mode(self, value):
		self.simple_mode = value;
	
	def set_liblouis_mode(self, value):
		self.liblouis_mode = value

	def set_conventional_braille(self, value):
		self.conventional_braille = value

	def set_one_hand_mode(self, value):
		self.one_hand_mode = value

	def set_one_hand_conversion_delay(self, value):
		self.one_hand_conversion_delay = value*1/1000
	
	def set_liblouis_language(self,language):
		self.last_loaded_liblouis_language = language
		self.liblouis_mode = True
		self.language_liblouis, notify_language = self.liblouis_language_table_conversion_dict[language]
		self.set_notify_language(notify_language)
		self.notify_text(language)
		
	def set_built_in_language(self,language):
		self.last_loaded_built_in_language = language
		self.liblouis_mode = False
		self.load_built_in_table(language)
		self.set_notify_language(self.built_in_language_notify_language_conversion_dict[language])
		self.notify_text(language)

	def set_checked_languages_built_in(self, list_):
		self.checked_languages_built_in = list_
		
	def set_checked_languages_liblouis(self, list_):
		self.checked_languages_liblouis = list_
	
	def set_get_text_before_cursor_callback(self, function):
		self.get_text_before_cursor = function

	def set_delete_text_before_cursor_callback(self, function):
		self.delete_text_before_cursor = function

	def set_insert_text_at_cursor_callback(self, function):
		self.insert_text_at_cursor = function

	def set_event_callback(self, function):
		self.event_callback = function
	
	def call_event_callback(self):
		if(self.event_callback != None):
			self.event_callback()
	
	def reset(self):
		self.pressed_key_list = []
		self.last_appeared_word_length = 0;
		self.louis_typing_word_combinations = "";
		self.braille_letter_map_pos = 0;
		self.capital_shift = 0;
		self.caps_lock = 0
		self.language_switch_built_in_mode= False
		self.is_liblouis_typing = False

	def toggle_braille_mode(self):
		self.braille_mode = not self.braille_mode
		self.reset()
		if(self.braille_mode):
			self.notify_text(_("Switched to Braille input"));
		else:
			self.notify_text(_("Switched to System input"));
		

	def set_braille_mode(self, value):
		self.braille_mode = value;
		self.last_appeared_word_length = 0;
		self.louis_typing_word_combinations = "";

	def set_notification(self, value):
		self.notification = value

	def notify_text(self, text, verbose=False):
		if(self.notification):
			self.notify_function(text, verbose)

	def set_notify_callback(self, function):
		self.notify_function = function

	def set_notify_language_callback(self, function):
		self.set_notify_language = function
		
	def key_pressed(self,event):		
		self.get_text_before_cursor(20)
		keycode = event.hardware_keycode;
		print("Keycode = "+str(keycode))

		if keycode in self.keycode_map.keys():
			pressed_key = self.keycode_map[keycode]
			print("Key = "+str(pressed_key))
			
			if ( pressed_key == Keys.ToggleBrailleMode):
				self.toggle_braille_mode()
				return False

			# Passing if not in braille mode
			if (not self.braille_mode):
				if((pressed_key == Keys.NewLine or pressed_key == Keys.NewLine2) and self.sigle_line_mode):
					return True
				else:
					return False
			
			# For making other shortcuts like Ctrl+A (select all) working 
			if(self.language_switch_built_in_mode and pressed_key not in [ Keys.L1, Keys.L2, Keys.L3, Keys.L4, Keys.L5, Keys.L6, Keys.L7, Keys.L8, Keys.L9, Keys.L10, Keys.L11, Keys.L12] ):
				return False
			
			clear_current_typing_variable = False

			# Storing pressed dots
			if(pressed_key in [ Keys.Dot1, Keys.Dot2, Keys.Dot3, Keys.Dot4, Keys.Dot5, Keys.Dot6, Keys.Dot7, Keys.Dot8, Keys.Capital, Keys.LetterDeletion ]):
				if (self.one_hand_mode):
					pass
					if (self.three_dot_pos == 1):
						self.pressed_key_list  += pressed_key
					else:
						self.pressed_key_list  += str(int(pressed_key)+3);
				else:
					self.pressed_key_list.append(pressed_key);
			
			# Language switching
			elif (pressed_key in self.language_key_list):
				clear_current_typing_variable=True
				self.is_liblouis_typing = False
				index = self.language_key_list.index(pressed_key);
				if(self.language_switch_built_in_mode):
					self.set_built_in_language(self.checked_languages_built_in[index])
				else:
					self.set_liblouis_language(self.checked_languages_liblouis[index])

			# Built-In language selector
			elif pressed_key == Keys.BuiltInSel:
				self.language_switch_built_in_mode= True
			
			# Space
			elif pressed_key == Keys.Space:
				clear_current_typing_variable=True
				self.is_liblouis_typing = False
				self.braille_letter_map_pos = 0;
				
				# Stop capitalizing new line start
				self.capitalize_line_start = False

				# To stop liblouis first letter capitalisation
				if(not self.caps_lock):
					self.capital_shift = 0

				# Checking sentence end for capitalization
				# Full Stop for English,  Devanagari, Sinhala, Chinese/Japanese, Urudu
				# '\u002e \u0964 \u0df4 '\u3002  u06d4
				# 63 -> ?                33 -> !
				# https://r12a.github.io/app-conversion/
				
				self.capitalize_sentence_start = False

				if(self.auto_capitalize_sentence):
					text = self.get_text_before_cursor(100)
					text = re.sub(' +', ' ', text)
					s = u'\u002e\u002c\u0021\u0964\u0df4\u3002\u06d4'
					print("###########"+text+"##############")
					for item in s:
						if(text.endswith(item)):
							self.capitalize_sentence_start = True

				if(not self.liblouis_mode):
					if (self.conventional_braille == True ):
						if(self.conventional_braille_dot_3):
							self.commit_string(self.map["3"][self.old_braille_letter_map_pos]);
							self.conventional_braille_dot_3 = False;
						if(self.conventional_braille_dot_4):
							self.conventional_braille_dot_4 = False;
							self.commit_string(self.map["4"][self.braille_letter_map_pos]);
						elif (self.conventional_braille_dot_4_pass == True):
							self.conventional_braille_dot_4_pass = False
							self.commit_string(self.map["8"][self.braille_letter_map_pos]);
				
				#Line limit info
				text = self.get_text_before_cursor(self.line_limit).split("\n")[-1]
				if( len(text) >= self.line_limit):
					if (self.auto_new_line and not self.sigle_line_mode):
						self.commit_string("\n");
						self.notify_text(_("new line"));
					else:
						self.commit_string(" ");
						self.notify_text(_("Limit exceeded"));
				else:
					self.commit_string(" ");
				self.call_event_callback()
			
### To-do : Say line number
			# New line
			elif((pressed_key == Keys.NewLine or pressed_key == Keys.NewLine2) and not self.sigle_line_mode):
				clear_current_typing_variable=True
				self.is_liblouis_typing = False
				self.commit_string("\n");
				self.notify_text(_("new line"));
				self.call_event_callback()
			
			
			elif (pressed_key == Keys.LangSwitch):
				clear_current_typing_variable=True
				if(self.liblouis_mode):
					self.language_iter_liblouis=(self.language_iter_liblouis+1)%len(self.checked_languages_liblouis);
					language_name = self.checked_languages_liblouis[self.language_iter_liblouis];
					self.language_liblouis, tts_language = self.liblouis_language_table_conversion_dict[language_name]
					self.set_notify_language(tts_language)
					self.notify_text(_("{} Loaded!").format(language_name));
				else:
					self.language_iter=(self.language_iter+1)%len(self.checked_languages);
					self.load_built_in_table(self.checked_languages[self.language_iter])
					
			elif (pressed_key == Keys.BegMidSwitch):
				if(self.liblouis_mode):
					self.reset()
				else:
					if (self.braille_letter_map_pos == 0):
						self.braille_letter_map_pos = 1;
					elif(self.braille_letter_map_pos == 1 or self.braille_letter_map_pos == 2):
						self.braille_letter_map_pos = 0;
					else:
						print("self.braille_letter_map_pos = "+str(self.braille_letter_map_pos))
						print(self.contractions_dict_inverse)
						previous_contraction_ordered_pressed_keys = self.contractions_dict_inverse[self.braille_letter_map_pos];
						print("previous_contraction_ordered_pressed_keys = "+str(previous_contraction_ordered_pressed_keys)) 
						if ("middle_" in previous_contraction_ordered_pressed_keys):
							self.braille_letter_map_pos = self.contractions_dict[previous_contraction_ordered_pressed_keys.replace("middle_" ,"")];
						elif("middle_" + previous_contraction_ordered_pressed_keys in self.contractions_dict):
							self.braille_letter_map_pos = self.contractions_dict.get("middle_" + previous_contraction_ordered_pressed_keys);
					
						print("Final self.braille_letter_map_pos = "+str(self.braille_letter_map_pos))


			if(clear_current_typing_variable):
				self.last_appeared_word_length = 0;
				self.louis_typing_word_combinations = "";
				self.braille_letter_map_pos = 0;
			
			return True
		else:
			self.last_appeared_word_length = 0;
			self.louis_typing_word_combinations = "";
			return False

		

	def key_released(self,event):
		# Passing if not in braille mode
		if (not self.braille_mode):
			return False
		
		# Filter processing of other keys
		keycode = event.hardware_keycode;
		if keycode not in self.keycode_map.keys():
			# Prevent liblouis letter deletion with combination if any other keys pressed
			self.is_liblouis_typing = False			
			return False

		# Getting released key list and current released key
		ordered_pressed_keys = self.order_pressed_keys(self.pressed_key_list);
		released_key = self.keycode_map[keycode]

		print("Released key " + str(released_key) )
		print("Orderd keys " + str( ordered_pressed_keys))
		
		# Remove built-in selection latch
		if (released_key == Keys.BuiltInSel):
			self.language_switch_built_in_mode= False
			self.is_liblouis_typing = False
			return True	
			
		#Toggle Punctuation
		elif (released_key == Keys.Punctuation):
			self.is_liblouis_typing = False
			self.braille_letter_map_pos = 2;
			
		#Expand Abbreviation
		elif (released_key ==  Keys.Abbreviation):
			self.is_liblouis_typing = False

			surrounding_text = self.get_text_before_cursor(20)
			last_word = surrounding_text.split()[-1]

			if ((self.simple_mode == 1 and not self.liblouis_mode)
			 or (surrounding_text[-1] == " ")):
				return False;
								
			#Substitute user abbreviation first, if not try built_in  
			if (last_word in self.abbreviations.keys()):
				self.delete_text_before_cursor(len(last_word));
				self.commit_string(self.abbreviations[last_word])
				self.call_event_callback()
				self.reset()

			elif (not self.liblouis_mode and last_word in self.built_in_abbreviations.keys()):
				self.delete_text_before_cursor(len(last_word));
				self.commit_string(self.built_in_abbreviations[last_word])
				self.call_event_callback()
				self.reset()
			
			# Move map position to middle
			if(not self.liblouis_mode):
				self.braille_letter_map_pos = 1;

		#Delete Last word
		elif (ordered_pressed_keys ==  [Keys.Capital, Keys.LetterDeletion]):
			self.is_liblouis_typing = False
			string_up_to_cursor = self.get_text_before_cursor(20)
				
			#If end is space, then count backword till a space found  			
			if (string_up_to_cursor[-1] == " "):
				count = 0
				char_found = 0;
					
				for item in string_up_to_cursor[::-1]:
					if (item != " "):
						char_found = 1;
					if (item == " " and char_found == 1):
						break;
					count += 1
				self.delete_text_before_cursor(count);
				self.notify_text(string_up_to_cursor[-(count):]+_("Deleted"))
				self.call_event_callback()	
			
			#If end is not space, delete length of last word	
			else:
				count = len(string_up_to_cursor.split()[-1])
				self.delete_text_before_cursor(count);
				self.notify_text(string_up_to_cursor.split()[-1]+_("Deleted"))
				self.call_event_callback()
			
			self.last_appeared_word_length = 0;
			self.louis_typing_word_combinations = "";


		#Delete Last letter
		elif ( ordered_pressed_keys == [Keys.LetterDeletion]):
			surrounding_text = self.get_text_before_cursor(20)
			if(not surrounding_text == ""):
				# Check 3 : self.louis_typing_word_combinations - for deleting space and new line				
				if (self.liblouis_mode and self.is_liblouis_typing and self.louis_typing_word_combinations != "" ):
					# Deleting last appeared word
					self.delete_text_before_cursor(self.last_appeared_word_length);
					
					# Remove last typed braille character
					self.louis_typing_word_combinations = self.louis_typing_word_combinations[:-1] 

					# Translating typing combinations
					word = louis.backTranslate(['unicode.dis',self.language_liblouis],self.louis_typing_word_combinations,None,0)
					result = word[0];

					# Storing length of result for deleting on
					self.last_appeared_word_length = len(result);

					# Commiting resut
					self.commit_string(result);
				else:
					self.delete_text_before_cursor(1);	
					self.notify_text(surrounding_text[-1:]+_("Deleted"))
					self.last_appeared_word_length = 0;
					self.louis_typing_word_combinations = "";


		#Toggle capital switch
		elif (ordered_pressed_keys == [Keys.Capital]):
			self.is_liblouis_typing = False
			if (self.capital_shift == 1):
				if (self.caps_lock == False):
					self.caps_lock = True
					self.notify_text(_("Caps Lock On!"))
				else:
					self.caps_lock = False
					self.notify_text(_("Caps Lock Off!"))
					self.capital_shift = 0;
			else:
				self.notify_text(_("Shift On!"))
				self.capital_shift = 1;


			
		else:
			if (len(ordered_pressed_keys) > 0):
				
				ordered_pressed_keys_in_string = u""
				for key in ordered_pressed_keys:
					if (key not in [Keys.LetterDeletion, Keys.Capital]):
						ordered_pressed_keys_in_string += key.value
				
				if (self.liblouis_mode):
					print("Liblouis mode"+self.language_liblouis)
					sum = 0
					for i in ordered_pressed_keys_in_string:
						sum = sum + pow(2,int(i)-1);
					pressed_dots = 0x2800 + sum

					# Adding last typed combination to list
					self.louis_typing_word_combinations = self.louis_typing_word_combinations + chr(pressed_dots)

					# Deleting last appeared word
					self.delete_text_before_cursor(self.last_appeared_word_length);

					# Translating typing combinations
					word = louis.backTranslate(['unicode.dis',self.language_liblouis],self.louis_typing_word_combinations,None,0)
					result = word[0];

					# Storing length of result for deleting on
					self.last_appeared_word_length = len(result);

					# Commiting resut
					self.commit_string(result);
					
					self.is_liblouis_typing = True 

				else: # Built-in mode
					
					#Move map position to middle  contraction if any 
					if (self.braille_letter_map_pos != 0 and "middle_"+ordered_pressed_keys_in_string in self.contractions_dict.keys() and self.one_hand_mode == False):
						self.braille_letter_map_pos = self.contractions_dict["middle_"+ordered_pressed_keys_in_string];

					#Move map position to contraction if any
					elif (ordered_pressed_keys_in_string in self.contractions_dict.keys() and self.one_hand_mode == False):
						self.braille_letter_map_pos = self.contractions_dict[ordered_pressed_keys_in_string];
					
					elif ( self.conventional_braille and ordered_pressed_keys == [Keys.Dot3]):
						self.conventional_braille_dot_3 = True;
						self.old_braille_letter_map_pos = self.braille_letter_map_pos
					
					elif( self.conventional_braille and ordered_pressed_keys == [Keys.Dot4] ):
						self.conventional_braille_dot_4 = True;

					else:
						if (self.one_hand_mode):
							if (self.three_dot_pos == 1 and self.pressed_key_list != ""):
								if (self.pressed_key_list == "o"):
									self.pressed_key_list = "";
								self.three_dot_pos = 2;
								t = Timer(self.one_hand_conversion_delay, self.three_dot_do_commit)
								t.start()
							return False

						try:
							value = self.map[ordered_pressed_keys_in_string][self.braille_letter_map_pos]
						except:
							value = "";
						

						
						
						
						self.commit_string(value);

						self.conventional_braille_dot_4_pass = False;
						self.conventional_braille_dot_3 = False;
						if (self.conventional_braille == 1 and self.conventional_braille_dot_4):
							self.conventional_braille_dot_4 = False;
							self.commit_string(self.map["4"][self.braille_letter_map_pos]);
							self.conventional_braille_dot_4_pass = True;
						self.braille_letter_map_pos = 1;
		self.pressed_key_list = [];
		return False




	def load_built_in_table(self,language):
		self.language = language
		print ("loading Map for language : %s" %self.language)
		self.map = {}
		submap_number = 1;
		self.append_sub_map("beginning.txt",submap_number);
		submap_number = 2;
		self.append_sub_map("middle.txt",submap_number);
		submap_number = 3;
		self.append_sub_map("punctuations.txt",submap_number);
		
		#Contraction dict 
		self.contractions_dict = {};
		
		#load each contractions to map
		for text_file in os.listdir("%s/%s/"%(built_in_braille_table_dir,self.language)):
			if text_file not in ["beginning.txt","middle.txt","abbreviations.txt","punctuations.txt"]:
				if (self.simple_mode == 0 and "~" not in text_file):
					submap_number += 1;
					self.append_sub_map(text_file,submap_number);
					self.contractions_dict[text_file[:-4]] = submap_number-1;
		print(self.contractions_dict)
		print(self.map)
		
		# For list switching
		self.contractions_dict_inverse = {v: k for k, v in self.contractions_dict.items()}
		  
		#Load abbreviations if exist
		self.built_in_abbreviations = {}
		try:
			for line in open("%s/%s/abbreviations.txt"%(built_in_braille_table_dir,self.language),mode='r'):
				self.built_in_abbreviations[line.split("  ")[0]] = line.split("  ")[1][:-1]
		except IndexError:
			print("Built-in abbreviation loading failed "+line) 
		except FileNotFoundError:
			pass
		


	def append_sub_map(self,filename,submap_number):
		print("Loading sub map file for : %s with sn : %d " % (filename,submap_number))	
		for line in open("%s/%s/%s"%(built_in_braille_table_dir,self.language,filename),"r"):
			if (line.split(" ")[0]) in self.map.keys():
				self.map[line.split(" ")[0]].append(line.split(" ")[1][:-1])
				if len(self.map[line.split(" ")[0]]) != submap_number:
					print("Repeated on : ",line.split(" ")[0])
			else:
				list=[];
				for i in range (1,submap_number):
					list.append(" ");
				list.append(line.split(" ")[1][:-1]);
				self.map[line.split(" ")[0]] = list;
		
		for key in self.map.keys():
			if len(self.map[key]) < submap_number:
				self.map[key].append(" ");


	def order_pressed_keys(self,pressed_keys):
		ordered = []
		# default 	"f","d","s","j","k","l","z",".","a","g","h",";","t"]
		print(pressed_keys)
		for key in Keys:
			if key in pressed_keys:
				ordered.append(key);
		return ordered;    

	def commit_string(self, text):
		
		if(text == "\n"):
			self.capitalize_line_start = True
		
		if(self.capitalize_line_start and self.auto_capitalize_line):
			text = text.capitalize()
			if(not self.liblouis_mode):
				self.capitalize_line_start = False
			
		if(self.capitalize_sentence_start and self.auto_capitalize_sentence):
			text = text.capitalize()
			if(not self.liblouis_mode):
				self.capitalize_sentence_start = False
		
		if((self.auto_capitalize_sentence or self.auto_capitalize_line)):
			surrounding_text = self.get_text_before_cursor(20)
			if(surrounding_text == ""):
				text = text.capitalize()
			
		if (self.capital_shift == 1):
			text = text.capitalize()
			if(not self.liblouis_mode):
				self.capital_shift = 0

		if (self.caps_lock == 1):
			text = text.upper()



		# Inserting text
		self.insert_text_at_cursor(text);
		
		# Case 0 : When previous_result is empty, announce the new one.
        # Case 1 : When new result is less than the length of previous, announce the new one.
        # Case 2 : When the result is a concatenation over previous one, announce the concatenated text
		if(self.liblouis_mode):
			announce_text = "";
			if (len(text) < len(self.previous_announced_text) or len(self.previous_announced_text) == 0):
				announce_text = text
			else:
				print(text,"----",self.previous_announced_text)
				if (text.startswith(self.previous_announced_text)):
					announce_text = text[len(self.previous_announced_text):]
				else:
					announce_text = text[:]
			self.notify_text(announce_text, True);
			self.previous_announced_text = text
		elif (len(text) > 1):
			self.notify_text(text,True)

	def three_dot_do_commit(self):
		self.three_dot_pos = 1;
		ordered_pressed_keys = self.order_pressed_keys(self.pressed_key_list);
		self.pressed_key_list = []
		try:
			value = self.map[ordered_pressed_keys][self.braille_letter_map_pos]
			self.commit_string(value);
			self.braille_letter_map_pos = 1
		except:
			pass
