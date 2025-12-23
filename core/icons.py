"""
Icon Helper Module
Provides Font Awesome icons to replace emojis throughout the application
"""

# Font Awesome CDN link
FONT_AWESOME_CDN = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

# Icon mappings
ICONS = {
    # Navigation
    'home': '<i class="fas fa-home"></i>',
    'dashboard': '<i class="fas fa-chart-line"></i>',
    'search': '<i class="fas fa-search"></i>',
    'patients': '<i class="fas fa-users"></i>',
    'doctors': '<i class="fas fa-user-md"></i>',
    'appointments': '<i class="fas fa-calendar-check"></i>',
    'lab': '<i class="fas fa-flask"></i>',
    'prediction': '<i class="fas fa-brain"></i>',
    'reports': '<i class="fas fa-file-medical"></i>',
    'notifications': '<i class="fas fa-bell"></i>',
    'messages': '<i class="fas fa-envelope"></i>',
    'analytics': '<i class="fas fa-chart-bar"></i>',
    
    # Risk levels
    'risk_high': '<i class="fas fa-exclamation-circle" style="color: #ff4d4d;"></i>',
    'risk_medium': '<i class="fas fa-exclamation-triangle" style="color: #ffbe0b;"></i>',
    'risk_low': '<i class="fas fa-check-circle" style="color: #00ff88;"></i>',
    'risk_unknown': '<i class="fas fa-question-circle" style="color: #888;"></i>',
    
    # Medical
    'medical': '<i class="fas fa-stethoscope"></i>',
    'pill': '<i class="fas fa-pills"></i>',
    'syringe': '<i class="fas fa-syringe"></i>',
    'heartbeat': '<i class="fas fa-heartbeat"></i>',
    'lungs': '<i class="fas fa-lungs"></i>',
    'xray': '<i class="fas fa-x-ray"></i>',
    'microscope': '<i class="fas fa-microscope"></i>',
    
    # Actions
    'edit': '<i class="fas fa-edit"></i>',
    'delete': '<i class="fas fa-trash-alt"></i>',
    'save': '<i class="fas fa-save"></i>',
    'add': '<i class="fas fa-plus-circle"></i>',
    'download': '<i class="fas fa-download"></i>',
    'upload': '<i class="fas fa-upload"></i>',
    'print': '<i class="fas fa-print"></i>',
    'email': '<i class="fas fa-at"></i>',
    'phone': '<i class="fas fa-phone"></i>',
    'back': '<i class="fas fa-arrow-left"></i>',
    'forward': '<i class="fas fa-arrow-right"></i>',
    'refresh': '<i class="fas fa-sync-alt"></i>',
    
    # Status
    'success': '<i class="fas fa-check-circle" style="color: #00ff88;"></i>',
    'error': '<i class="fas fa-times-circle" style="color: #ff4d4d;"></i>',
    'warning': '<i class="fas fa-exclamation-triangle" style="color: #ffbe0b;"></i>',
    'info': '<i class="fas fa-info-circle" style="color: #00d9ff;"></i>',
    'loading': '<i class="fas fa-spinner fa-spin"></i>',
    
    # User
    'user': '<i class="fas fa-user"></i>',
    'male': '<i class="fas fa-mars"></i>',
    'female': '<i class="fas fa-venus"></i>',
    'birthday': '<i class="fas fa-birthday-cake"></i>',
    'id_card': '<i class="fas fa-id-card"></i>',
    
    # Time
    'clock': '<i class="fas fa-clock"></i>',
    'calendar': '<i class="fas fa-calendar-alt"></i>',
    'history': '<i class="fas fa-history"></i>',
    
    # Data
    'chart': '<i class="fas fa-chart-pie"></i>',
    'graph': '<i class="fas fa-chart-area"></i>',
    'table': '<i class="fas fa-table"></i>',
    'filter': '<i class="fas fa-filter"></i>',
    'sort': '<i class="fas fa-sort"></i>',
    
    # Communication
    'video': '<i class="fas fa-video"></i>',
    'chat': '<i class="fas fa-comments"></i>',
    
    # Files
    'file': '<i class="fas fa-file"></i>',
    'pdf': '<i class="fas fa-file-pdf"></i>',
    'image': '<i class="fas fa-image"></i>',
    'folder': '<i class="fas fa-folder"></i>',
    
    # Settings
    'settings': '<i class="fas fa-cog"></i>',
    'help': '<i class="fas fa-question-circle"></i>',
    'logout': '<i class="fas fa-sign-out-alt"></i>',
    'login': '<i class="fas fa-sign-in-alt"></i>',
}

def icon(name, size='1em', color=None, extra_class=''):
    """
    Get an icon by name
    
    Args:
        name: Icon name from ICONS dict
        size: Font size (e.g., '1.5em', '24px')
        color: Color override
        extra_class: Additional CSS classes
    
    Returns:
        HTML string for the icon
    """
    if name not in ICONS:
        return f'<span>?</span>'  # Fallback
    
    icon_html = ICONS[name]
    
    # Add custom styling
    style = f'font-size: {size};'
    if color:
        style += f' color: {color};'
    
    if 'style=' in icon_html:
        # Icon already has inline style
        icon_html = icon_html.replace('style="', f'style="{style} ')
    else:
        # Add style before closing >
        icon_html = icon_html.replace('></i>', f' style="{style}"></i>')
    
    if extra_class:
        icon_html = icon_html.replace('class="', f'class="{extra_class} ')
    
    return icon_html

def init_icons():
    """Initialize Font Awesome - call this at the start of each page"""
    return FONT_AWESOME_CDN

# Convenience functions
def success_icon(): return icon('success')
def error_icon(): return icon('error')
def warning_icon(): return icon('warning')
def info_icon(): return icon('info')
def loading_icon(): return icon('loading')

def risk_icon(level):
    """Get risk icon based on level"""
    level_map = {
        'HIGH': 'risk_high',
        'MEDIUM': 'risk_medium',
        'LOW': 'risk_low',
    }
    return icon(level_map.get(level.upper(), 'risk_unknown'))
