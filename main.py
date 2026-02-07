from playwright.sync_api import sync_playwright
import json
import time
from model.chat import Message
from dataclasses import asdict

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
        
        
        calendar_icon = page.locator("span[data-icon='calendar-filled-refreshed']")
        
        calendar_icon.click()   
        
        previus_month = page.locator("button[aria-label='Mes anterior']")
        
        previus_month.click()
        
        january_1 = page.locator("abbr[aria-label='1 de enero de 2026']")
        
        january_1.click()
        
        time.sleep(3)
        
        
        container_messages = page.locator("div.x3psx0u.x12xbjc7.x1c1uobl.xrmvbpv.xh8yej3.xquzyny.xvc5jky.x11t971q")
        
        children = container_messages.locator(":scope > div")
        
        current_date = None
        messages_data: list[Message] = []
        
        
        for i in range(children.count()):
            print(f"Processing message {i+1}/{children.count()}")
            
            
            el = children.nth(i)
            
            class_name = el.get_attribute("class") or ""
            
            if "focusable-list-item" in class_name:
                current_date = el.inner_text().strip()
                print("DATE:", current_date)
                continue
            
            messages = el.locator("div[role='row']")
            
            
            if messages.count() == 0:
                continue
            
            message_location = messages.all()

            for message_raw in message_location:
                from_me = True
                
                find_out = message_raw.locator("div.message-out.focusable-list-item._amjy._amjz._amjw.x1klvx2g.xahtqtb")
                if find_out.count() == 0:
                    from_me = False
            
                audio = message_raw.locator("span[data-icon='audio-download']")
                if audio.count() > 0:
                    print("This is an audio message.")
                    new_messsage = Message(
                        type="audio",
                        text="Audio message",
                        status="sent",
                        date=current_date,
                        from_me=from_me
                    )
                    messages_data.append(new_messsage)
                    continue
                
                is_citation = message_raw.locator("div[aria-label='Mensaje citado']").count() > 0
                
                idx_label = 0
                
                if is_citation:
                    idx_label = 1
                
                text = message_raw.locator("span[data-testid='selectable-text']")
                if text.count() > 0:
                    text_content = text.nth(idx_label).all_inner_texts()
                    new_messsage = Message(
                        type="text",
                        text=" ".join(text_content),
                        status="sent",
                        date=current_date,
                        from_me=from_me
                    )
                    messages_data.append(new_messsage)
                    continue
                    
            print(f"Messages for {current_date}: {messages.count()}")
        
        print(f"Total messages collected: {len(messages_data)}")
        with open("messages_data.json", "w") as f:
                json.dump([asdict(m) for m in messages_data], f, indent=4, ensure_ascii=False)
                

        
        input("Press Enter to continue to the next chat...")
    
    input("Press Enter to end the session...")    
