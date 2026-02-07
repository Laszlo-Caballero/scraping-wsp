from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="./user_data",
        headless=False,
        args=["--start-maximized"]
    )
    page = context.new_page()
    page.goto("https://web.whatsapp.com")
    page.evaluate("document.body.style.zoom='80%'")
    
    input("Please scan the QR code and press Enter to continue...")
    # Get all chat elements    
    
    main = page.locator("#main")
    
    chats = page.locator("div[role='row']").all()
    
    
    ## FOR TESTING PURPOSES ONLY: Click the first chat
    for chat in chats:
        chat.click() 
        header = main.locator("header")
        header.click()
            
        isGroup = page.locator("div[role='complementary']").count() > 0
        print(f"Is this a group chat? {'Yes' if isGroup else 'No'}")
        
        if isGroup:
            continue
        
        container_data = page.locator(
        "div.x1c4vz4f.xs83m0k.xdl72j9.x1g77sc7.x78zum5.xozqiw3.x1oa3qoh.x12fk4p8.xeuugli.x2lwn1j.x1nhvcw1.xdt5ytf.x6s0dn4"
        )
        
        texts = container_data.locator("span").all_inner_texts()

        ##METADATA
        clean = []
        for t in texts:
            t = t.strip()
            if t and t not in clean:
                clean.append(t)

        
        ## FLOW 1/01/2026
        
        button_search = page.locator("button[aria-label='Buscar']")
        
        button_search.click()
        
        
        
        container_messages = page.locator("div.x3psx0u.x12xbjc7.x1c1uobl.xrmvbpv.xh8yej3.xquzyny.xvc5jky.x11t971q")
        
        date = container_messages.locator("div.focusable-list-item").first.inner_text()
        print(f"Date of the first message: {date}")
        
        input("Press Enter to continue to the next chat...")
    
    
    
    
    
    
    input("Press Enter to end the session...")    
