import asyncio
from playwright.async_api import async_playwright
import time
from model.chat import MessageDto
from dataclasses import asdict
from db.utils import create_session, create_tables
from crud.crud import ChatCrud, MessageCrud
from enums.status_enum import StatusEnum

create_tables()

session = create_session()

chat_crud = ChatCrud(session)
message_crud = MessageCrud(session)

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            headless=False,
            args=["--start-maximized"]
        )
        page = await context.new_page()
        await page.goto("https://web.whatsapp.com")
        await page.evaluate("document.body.style.zoom='80%'")
        
        input("Please scan the QR code and press Enter to continue...")
        # Get all chat elements    
        
        main = page.locator("#main")
        count_check_chats = True
        count_chats_checked = 0
        while count_check_chats:
            print("Checking chats...")
            
            scroll_chat = page.locator("#pane-side")
            
            
  
            
            chats =  scroll_chat.locator("div.x10l6tqk.xh8yej3.x1g42fcv")

  
            
            count = await chats.count()
            is_pause_chats = 0
            ## FOR TESTING PURPOSES ONLY: Click the first chat
            
            input("Press Enter to start checking chats...")
            
            await page.evaluate("""
                        () => {
                            if (!window.__wsp_idx) window.__wsp_idx = 0;
                            const chats = document.querySelectorAll("div.x10l6tqk.xh8yej3.x1g42fcv:not([wsp-scrap])");
                            chats.forEach(el => {
                                el.setAttribute("wsp-scrap", window.__wsp_idx++);
                            });
                        }
                        """)

            max_idx = await page.evaluate("window.__wsp_idx")
            print("Total chats indexed:", max_idx)
            print(count)


            for y in range(count):
                chat = scroll_chat.locator(f"div[wsp-scrap='{y}']")

                if await chat.count() == 0:
                    print(f"div[wsp-scrap='{y}']")
                    print("No more chats to check.")
                    break
                
              
                
                print(f"Processing chat {y+1}/{await chats.count()}")
                print(await chat.get_attribute("check"))
                if await chat.get_attribute("check") == "false":
                    print("Already processed, skipping...")
                    count_chats_checked += 1
                    continue
            
                await chat.evaluate("""
                        el => {
                            el.setAttribute('check', 'true')
                            el.style.backgroundColor = '#ff0303'
                        }
                        """)
                
                
                
                await chat.click() 
                header = main.locator("header")
                await header.click()
                    
                isGroup = await page.locator("div[role='complementary']").count() > 0
                print(f"Is this a group chat? {'Yes' if isGroup else 'No'}")
                
                if isGroup:
                    continue
                
                container_data = page.locator(
                "div.x1c4vz4f.xs83m0k.xdl72j9.x1g77sc7.x78zum5.xozqiw3.x1oa3qoh.x12fk4p8.xeuugli.x2lwn1j.x1nhvcw1.xdt5ytf.x6s0dn4"
                )
                
                texts = await container_data.locator("span").all_inner_texts()

                ##METADATA
                clean = []
                for t in texts:
                    t = t.strip()
                    if t and t not in clean:
                        clean.append(t)

                name = clean[0] if len(clean) > 0 else None
                phone = clean[1] if len(clean) > 1 else None
                
                
                if name is None or phone is None:
                    name_enterprise = page.locator(".xlm9qay.x1s688f.x1e56ztr")
                    if await name_enterprise.count() > 0:
                        name = (await name_enterprise.inner_text()).strip()
                    else:
                        name = "Unknown"
                    
                    phone_enterprise = page.locator(".x1iyjqo2.xs83m0k.xdl72j9.x1rdy4ex.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft")
                    if await phone_enterprise.count() > 0:
                        phone = (await phone_enterprise.inner_text()).strip()
                    else:
                        phone = "Unknown"
                    
                    
                        
                
                chat = chat_crud.create_chat(name=name, phone=phone)
                continue
                
                
                
                ## FLOW 1/01/2026
                button_search = page.locator("button[aria-label='Buscar']")
                await button_search.click()
                
                
                calendar_icon = page.locator("span[data-icon='calendar-filled-refreshed']")
                
                await calendar_icon.click()   
                
                previus_month = page.locator("button[aria-label='Mes anterior']")
                
                await previus_month.click()
                
                january_1 = page.locator("abbr[aria-label='1 de enero de 2026']")
                
                await january_1.click()
                
                await asyncio.sleep(0.5)
                
                count_checked = True
                count_messages_checked = 0
                
                scroll = page.locator("div[data-scrolltracepolicy='wa.web.conversation.messages']")
                is_pause = 0
                
                while count_checked:
                    print("Checking messages...")
                    container_messages = page.locator("div.x3psx0u.x12xbjc7.x1c1uobl.xrmvbpv.xh8yej3.xquzyny.xvc5jky.x11t971q")
                    children = container_messages.locator(":scope > div")
                    
                    current_date = None
                    
                    child_all = await children.all()
                    
                    
                    for i, el in enumerate(child_all):
                        
                        if await el.count() == 0:
                            print("No more messages to check.")
                            continue
                        
                        if count_messages_checked ==  await children.count():
                            break
                        
                        print(f"Processing message {i+1}/{await children.count()}")
                        
                        
                        if await el.get_attribute("check") == "true":
                            print("Already processed, skipping...")
                            count_messages_checked += 1
                            continue
                        
                        await el.evaluate("""
                                    el => {
                                        el.setAttribute('check', 'true')
                                        el.style.backgroundColor = '#ff0303'
                                    }
                                    """)
                        
                        class_name = await el.get_attribute("class") or ""
                        
                        if "focusable-list-item" in class_name:
                            current_date = (await el.inner_text()).strip()
                            print("DATE:", current_date)
                            continue
                        
                        messages = el.locator("div[role='row']")
                        
                        
                        if await messages.count() == 0:
                            continue
                        
                        message_location = await messages.all()

                        for message_raw in message_location:
                            from_me = True
                            
                            send_type: StatusEnum = StatusEnum.NOT_VIEWED
                            
                            locale_view = message_raw.locator("span[aria-label=' Leído ']")
                            
                            if await locale_view.count() > 0:
                                send_type = StatusEnum.VIEWED
                            
                            
                            find_out = message_raw.locator("div.message-out.focusable-list-item._amjy._amjz._amjw.x1klvx2g.xahtqtb")
                            if await find_out.count() == 0:
                                from_me = False
                        
                            audio = message_raw.locator("span[data-icon='audio-download']")
                            if await audio.count() > 0:
                                print("This is an audio message.")
                                new_messsage = MessageDto(
                                    type="audio",
                                    text="Audio message",
                                    status=send_type,
                                    date=current_date,
                                    from_me=from_me
                                )
                                message_crud.create_message(new_messsage, chat)
                                continue
                            
                            is_citation = await message_raw.locator("div[aria-label='Mensaje citado']").count() > 0
                            
                            idx_label = 0
                            
                            if is_citation:
                                idx_label = 1
                            
                            text = message_raw.locator("span[data-testid='selectable-text']")
                            if await text.count() > 0:
                                text_content = await text.nth(idx_label).all_inner_texts()
                                new_messsage = MessageDto(
                                    type="text",
                                    text=" ".join(text_content),
                                    status=send_type,
                                    date=current_date,
                                    from_me=from_me
                                )
                                message_crud.create_message(new_messsage, chat)
                                continue
                                
                        print(f"Messages for {current_date}: {await messages.count()}")
                        
                    
                    await scroll.evaluate("el => el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })")
                    
                    
                    is_pause += 1
                    
                    if is_pause == 20:
                        count_checked = False
                        
            
            is_pause_chats += 1
            
            if is_pause_chats == 5:
                isTrue_chats = input("Do you want to check for more chats? (y/n): ")
                if isTrue_chats.lower() != "y":
                    count_check_chats = False
                else:
                    is_pause_chats = 0
            
                
        input("Press Enter to end the session...")    


asyncio.run(main())