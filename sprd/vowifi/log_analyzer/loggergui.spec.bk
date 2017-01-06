# -*- mode: python -*-

block_cipher = None


a = Analysis(['loggergui.py'],
             pathex=['D:\\code\\github\\myLab\\sprd\\vowifi\\log_analyzer'],
             binaries=[('config.ini', '.'), ('font', './font'), ('C:\\Python27\\Lib\\site-packages\\mobile_codes\\json\\*.json', 'mobile_codes/json/')],
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='loggergui',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='loggergui')
