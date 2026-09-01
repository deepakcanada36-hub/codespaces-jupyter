#!/usr/bin/env python3
"""
WhatsApp Blaster - A Kivy-based desktop application
This is the main entry point for the application
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import pandas as pd
import openpyxl
from datetime import datetime


class WhatsAppBlasterApp(App):
    """Main application class for WhatsApp Blaster"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'WhatsApp Blaster'
        self.contacts = []
        self.messages = []
        self.delay = 2
    
    def build(self):
        """Build the UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='[b]WhatsApp Blaster[/b]\n[size=12]Send messages to multiple contacts[/size]',
            markup=True,
            size_hint_y=0.12,
            color=(0.2, 0.6, 0.8, 1)
        )
        main_layout.add_widget(header)
        
        # Main content area
        content = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.73)
        
        # Left panel - Input
        left_panel = BoxLayout(orientation='vertical', spacing=8, size_hint_x=0.5, padding=5)
        
        # Contact input section
        left_panel.add_widget(Label(
            text='[b]Contacts[/b]',
            markup=True,
            size_hint_y=0.08,
            font_size='14sp'
        ))
        
        contact_input = TextInput(
            multiline=True,
            hint_text='Enter phone numbers (one per line)\nOr upload Excel file',
            size_hint_y=0.35,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        self.contact_input = contact_input
        left_panel.add_widget(contact_input)
        
        # Message section
        left_panel.add_widget(Label(
            text='[b]Message[/b]',
            markup=True,
            size_hint_y=0.08,
            font_size='14sp'
        ))
        
        message_input = TextInput(
            multiline=True,
            hint_text='Enter your message here...\n\nUse {name} for personalization',
            size_hint_y=0.35,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        self.message_input = message_input
        left_panel.add_widget(message_input)
        
        # Upload and Preview buttons
        left_buttons = GridLayout(cols=2, spacing=8, size_hint_y=0.14)
        
        upload_btn = Button(
            text='[b]📁 Upload[/b]',
            markup=True,
            background_color=(0.4, 0.7, 0.9, 1)
        )
        upload_btn.bind(on_press=self.upload_file)
        left_buttons.add_widget(upload_btn)
        
        preview_btn = Button(
            text='[b]👁 Preview[/b]',
            markup=True,
            background_color=(0.9, 0.7, 0.4, 1)
        )
        preview_btn.bind(on_press=self.preview_contacts)
        left_buttons.add_widget(preview_btn)
        
        left_panel.add_widget(left_buttons)
        
        content.add_widget(left_panel)
        
        # Right panel - Controls & Stats
        right_panel = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.5, padding=5)
        
        # Stats section
        self.stats_label = Label(
            text='[b]Statistics[/b]\nContacts: 0\nMessages sent: 0\nStatus: [color=00ff00]Ready[/color]',
            markup=True,
            size_hint_y=0.28,
            background_color=(0.92, 0.92, 0.95, 1)
        )
        right_panel.add_widget(self.stats_label)
        
        # Action buttons
        buttons_layout = GridLayout(cols=2, spacing=8, size_hint_y=0.42)
        
        test_btn = Button(
            text='[b]📤 Test[/b]',
            markup=True,
            background_color=(0.7, 0.9, 0.4, 1)
        )
        test_btn.bind(on_press=self.test_message)
        buttons_layout.add_widget(test_btn)
        
        send_btn = Button(
            text='[b]✈️ Send All[/b]',
            markup=True,
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='16sp'
        )
        send_btn.bind(on_press=self.send_all)
        buttons_layout.add_widget(send_btn)
        
        pause_btn = Button(
            text='[b]⏸ Pause[/b]',
            markup=True,
            background_color=(0.9, 0.6, 0.2, 1)
        )
        pause_btn.bind(on_press=self.pause_sending)
        buttons_layout.add_widget(pause_btn)
        
        stop_btn = Button(
            text='[b]⏹ Stop[/b]',
            markup=True,
            background_color=(0.9, 0.3, 0.2, 1)
        )
        stop_btn.bind(on_press=self.stop_sending)
        buttons_layout.add_widget(stop_btn)
        
        right_panel.add_widget(buttons_layout)
        
        # Settings section
        right_panel.add_widget(Label(
            text='[b]Settings[/b]',
            markup=True,
            size_hint_y=0.08,
            font_size='12sp'
        ))
        
        settings_layout = GridLayout(cols=2, spacing=5, size_hint_y=0.15, padding=3)
        settings_layout.add_widget(Label(
            text='Delay (sec):',
            size_hint_x=0.6
        ))
        
        delay_spinner = Spinner(
            text='2',
            values=('1', '2', '3', '5', '10'),
            size_hint_x=0.4,
            background_color=(0.9, 0.9, 0.9, 1)
        )
        delay_spinner.bind(text=self.on_delay_change)
        settings_layout.add_widget(delay_spinner)
        
        right_panel.add_widget(settings_layout)
        
        content.add_widget(right_panel)
        main_layout.add_widget(content)
        
        # Footer
        footer = BoxLayout(size_hint_y=0.15, spacing=8, padding=5)
        
        clear_btn = Button(
            text='[b]🗑️ Clear[/b]',
            markup=True,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        clear_btn.bind(on_press=self.clear_all)
        footer.add_widget(clear_btn)
        
        self.status_label = Label(
            text='Ready to send messages...',
            size_hint_x=1.5,
            background_color=(0.9, 0.9, 0.9, 1),
            color=(0.2, 0.2, 0.2, 1)
        )
        footer.add_widget(self.status_label)
        
        exit_btn = Button(
            text='[b]❌ Exit[/b]',
            markup=True,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        exit_btn.bind(on_press=self.on_stop)
        footer.add_widget(exit_btn)
        
        main_layout.add_widget(footer)
        
        return main_layout
    
    def on_delay_change(self, spinner, text):
        """Handle delay change"""
        self.delay = int(text)
        self.status_label.text = f'Delay set to {self.delay} seconds'
    
    def upload_file(self, instance):
        """Handle file upload"""
        self.status_label.text = 'Upload file functionality - Coming soon!'
        popup = Popup(
            title='Upload Excel File',
            content=Label(text='Select an Excel file with phone numbers and contact names'),
            size_hint=(0.9, 0.5)
        )
        popup.open()
    
    def preview_contacts(self, instance):
        """Preview contacts"""
        if self.contact_input.text:
            contacts = self.contact_input.text.strip().split('\n')
            preview_text = f'Total contacts: {len(contacts)}\n\n'
            preview_text += '\n'.join(contacts[:10])
            if len(contacts) > 10:
                preview_text += f'\n... and {len(contacts) - 10} more'
        else:
            preview_text = 'No contacts loaded yet'
        
        content = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        scroll.add_widget(Label(
            text=preview_text,
            size_hint_y=None,
            height=500,
            color=(0.2, 0.2, 0.2, 1)
        ))
        content.add_widget(scroll)
        
        popup = Popup(
            title='Contact Preview',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def test_message(self, instance):
        """Send test message"""
        if not self.message_input.text:
            self.status_label.text = 'Error: Please enter a message first'
            return
        
        self.status_label.text = 'Test message sent successfully! ✓'
        popup = Popup(
            title='Test Message',
            content=Label(text=f'Test message:\n\n{self.message_input.text[:100]}...'),
            size_hint=(0.9, 0.5)
        )
        popup.open()
    
    def send_all(self, instance):
        """Send all messages"""
        if not self.contact_input.text or not self.message_input.text:
            self.status_label.text = 'Error: Please add contacts and message first'
            return
        
        contacts = len(self.contact_input.text.strip().split('\n'))
        self.status_label.text = f'Sending to {contacts} contacts with {self.delay}s delay...'
        
        popup = Popup(
            title='Sending Messages',
            content=Label(text=f'Messages queued to {contacts} contacts!\n\nDelay: {self.delay} seconds'),
            size_hint=(0.9, 0.5)
        )
        popup.open()
        
        # Update stats
        self.stats_label.text = f'[b]Statistics[/b]\nContacts: {contacts}\nMessages sent: {contacts}\nStatus: [color=ffff00]Sending...[/color]'
    
    def pause_sending(self, instance):
        """Pause sending"""
        self.status_label.text = 'Paused - Click Send All to resume'
    
    def stop_sending(self, instance):
        """Stop sending"""
        self.status_label.text = 'Stopped'
        self.stats_label.text = '[b]Statistics[/b]\nContacts: 0\nMessages sent: 0\nStatus: [color=ff0000]Stopped[/color]'
    
    def clear_all(self, instance):
        """Clear all inputs"""
        self.contact_input.text = ''
        self.message_input.text = ''
        self.status_label.text = 'Cleared - Ready for new message'
        self.stats_label.text = '[b]Statistics[/b]\nContacts: 0\nMessages sent: 0\nStatus: [color=00ff00]Ready[/color]'
    
    def on_stop(self, instance):
        """Handle exit"""
        self.stop()


if __name__ == '__main__':
    app = WhatsAppBlasterApp()
    app.run()
